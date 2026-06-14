from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from loguru import logger

from retrieval.rag_chain import get_rag_chain

from .eval_config import GOLD_QA_PATH, RESULTS_DIR, SUMMARIES_DIR, resolve_path
from .dataset import EvalItem, load_eval_dataset
from .judge import GeminiJudge, JudgeResult, calculate_overall_band, normalize_answer_type
from .scoring import ScoredItem, build_summary


def _iso_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _format_context(docs: list[dict]) -> str:
    if not docs:
        return "No retrieved sources"
    lines = []
    for i, d in enumerate(docs, 1):
        lines.append(f"[{i}] {d.get('subject','')}|{d.get('grade','')} {d.get('topic','')} > {d.get('section','')}")
        url = d.get("url", "")
        if url:
            lines.append(f"URL: {url}")
        content = str(d.get("content", "")).strip()
        if content:
            lines.append("Content:")
            lines.append(content)
    return "\n".join(lines)


def _run_item(item: EvalItem, judge: GeminiJudge) -> ScoredItem:
    chain = get_rag_chain()
    model_answer = chain.ask(
        item.question,
        subject=item.subject,
        grade=item.grade,
        preferred_answer_type=item.preferred_answer_type,
        language=item.language,
        keypoints=item.keypoints,
    )
    context_docs = chain.get_context_docs(
        item.question,
        subject=item.subject,
        grade=item.grade,
        language=item.language,
        keypoints=item.keypoints,
    )
    context = _format_context(context_docs)
    judge_result = judge.score(
        question=item.question,
        reference_answer=item.reference_answer,
        model_answer=model_answer,
        context=context,
        preferred_answer_type=item.preferred_answer_type,
    )

    return ScoredItem(
        item_id=item.id,
        subject=item.subject or "",
        grade=item.grade or "",
        question=item.question,
        reference_answer=item.reference_answer,
        preferred_answer_type=item.preferred_answer_type,
        language=item.language,
        keypoints=item.keypoints,
        model_answer=model_answer,
        retrieved_context=context,
        scores=judge_result,
        overall_band=judge_result.overall_band,
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _scored_item_to_row(s: ScoredItem) -> dict[str, Any]:
    return {
        "id": s.item_id,
        "subject": s.subject,
        "grade": s.grade,
        "question": s.question,
        "reference_answer": s.reference_answer,
        "preferred_answer_type": s.preferred_answer_type,
        "language": s.language,
        "keypoints": s.keypoints,
        "model_answer": s.model_answer,
        "retrieved_context": s.retrieved_context,
        "scores": asdict(s.scores),
        "overall_band": s.overall_band,
    }


def _write_summary(path: Path, summary: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def _row_to_scored_item(row: dict[str, Any]) -> ScoredItem:
    scores = dict(row.get("scores") or {})
    if "type_alignment" not in scores and "safety" in scores:
        scores["type_alignment"] = scores["safety"]

    for key in ["correctness", "groundedness", "completeness", "clarity", "type_alignment"]:
        value = scores.get(key, 1)
        scores[key] = value if isinstance(value, int) and not isinstance(value, bool) else 1

    scores["target_answer_type"] = normalize_answer_type(scores.get("target_answer_type"))
    scores["detected_answer_type"] = normalize_answer_type(scores.get("detected_answer_type"))
    scores["rationale"] = str(scores.get("rationale", ""))
    scores["overall_band"] = calculate_overall_band(
        scores["correctness"],
        scores["groundedness"],
        scores["completeness"],
        scores["clarity"],
        scores["type_alignment"],
    )

    judge_result = JudgeResult(
        correctness=scores["correctness"],
        groundedness=scores["groundedness"],
        completeness=scores["completeness"],
        clarity=scores["clarity"],
        type_alignment=scores["type_alignment"],
        target_answer_type=scores["target_answer_type"],
        detected_answer_type=scores["detected_answer_type"],
        overall_band=scores["overall_band"],
        rationale=scores["rationale"],
    )

    return ScoredItem(
        item_id=str(row.get("id", "")),
        subject=str(row.get("subject", "")),
        grade=str(row.get("grade", "")),
        question=str(row.get("question", "")),
        reference_answer=str(row.get("reference_answer", "")),
        preferred_answer_type=normalize_answer_type(row.get("preferred_answer_type")),
        language=str(row.get("language", "")),
        keypoints=str(row.get("keypoints", "")),
        model_answer=str(row.get("model_answer", "")),
        retrieved_context=str(row.get("retrieved_context", "")),
        scores=judge_result,
        overall_band=judge_result.overall_band,
    )


def _load_scored_items(path: Path) -> list[ScoredItem]:
    if not path.exists():
        raise FileNotFoundError(f"Resume file does not exist: {path}")

    items: list[ScoredItem] = []
    with open(path, encoding="utf-8-sig") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                items.append(_row_to_scored_item(row))
            except Exception as exc:
                raise ValueError(f"Invalid resume row {line_number} in {path}: {exc}") from exc
    return items


def _emit_console(summary: dict[str, Any]) -> None:
    logger.info("Eval complete")
    logger.info(f"Items: {summary['count']}")
    logger.info(f"Overall band: {summary['overall_band']}")
    logger.info(f"Pass rate: {summary['pass_rate']}% (threshold={summary['pass_threshold']})")
    metrics = summary.get("metric_averages", {})
    logger.info(
        "Metrics avg | "
        + " | ".join(
            f"{k}={v}" for k, v in metrics.items()
        )
    )


def run_evaluation(
    dataset_path: Optional[str | Path] = None,
    limit: Optional[int] = None,
    judge_model: Optional[str] = None,
    resume_from: Optional[str | Path] = None,
) -> dict[str, Any]:
    ds_path = resolve_path(dataset_path, GOLD_QA_PATH)
    items = load_eval_dataset(ds_path, limit=limit)

    judge = GeminiJudge(model=judge_model) if judge_model else GeminiJudge()
    if resume_from:
        results_path = Path(resume_from)
        timestamp = results_path.stem
        summaries_path = SUMMARIES_DIR / f"{timestamp}.json"
        scored_items = _load_scored_items(results_path)
        logger.info(f"Resuming evaluation from {results_path} with {len(scored_items)} completed items")
    else:
        timestamp = _iso_ts()
        results_path = RESULTS_DIR / f"{timestamp}.jsonl"
        summaries_path = SUMMARIES_DIR / f"{timestamp}.json"
        scored_items: list[ScoredItem] = []

    completed_ids = {item.item_id for item in scored_items if item.item_id}
    try:
        for item in items:
            if item.id in completed_ids:
                logger.info(f"Skipping completed item {item.id}")
                continue
            logger.info(f"Evaluating {item.id} [{item.subject}|{item.grade}]")
            scored_item = _run_item(item, judge)
            scored_items.append(scored_item)
            completed_ids.add(scored_item.item_id)
            _append_jsonl(results_path, _scored_item_to_row(scored_item))

            partial_summary = {
                "timestamp": timestamp,
                "status": "partial",
                "dataset_path": str(ds_path),
                "judge_model": judge.model,
                "results_path": str(results_path),
                "completed": len(scored_items),
                "total_requested": len(items),
                "resumed_from": str(resume_from) if resume_from else None,
                **build_summary(scored_items),
            }
            _write_summary(summaries_path, partial_summary)
    except Exception as exc:
        if scored_items:
            failed_summary = {
                "timestamp": timestamp,
                "status": "failed",
                "dataset_path": str(ds_path),
                "judge_model": judge.model,
                "results_path": str(results_path),
                "completed": len(scored_items),
                "total_requested": len(items),
                "resumed_from": str(resume_from) if resume_from else None,
                "error": str(exc),
                **build_summary(scored_items),
            }
            _write_summary(summaries_path, failed_summary)
            logger.error(
                f"Eval failed after {len(scored_items)}/{len(items)} items; "
                f"partial results saved to {results_path}"
            )
        raise

    summary = build_summary(scored_items)

    summary_blob = {
        "timestamp": timestamp,
        "status": "complete",
        "dataset_path": str(ds_path),
        "judge_model": judge.model,
        "results_path": str(results_path),
        "completed": len(scored_items),
        "total_requested": len(items),
        "resumed_from": str(resume_from) if resume_from else None,
        **summary,
    }
    _write_summary(summaries_path, summary_blob)

    _emit_console(summary_blob)
    return summary_blob


def _arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run offline LLM-based RAG evaluation")
    p.add_argument("--dataset", type=str, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--judge-model", type=str, default=None)
    p.add_argument("--resume-from", type=str, default=None)
    return p


def main() -> None:
    args = _arg_parser().parse_args()
    summary = run_evaluation(
        dataset_path=args.dataset,
        limit=args.limit,
        judge_model=args.judge_model,
        resume_from=args.resume_from,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
