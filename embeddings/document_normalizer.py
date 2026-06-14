from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from loguru import logger

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import NORMALIZED_DIR, RAW_DIR


THAI_RE = re.compile(r"[\u0E00-\u0E7F]")
SPACE_RE = re.compile(r"[ \t]{2,}")
NEWLINE_RE = re.compile(r"\n{3,}")
SLUG_RE = re.compile(r"[^a-z0-9]+")

REQUIRED_NORMALIZED_FIELDS = (
    "doc_id",
    "source",
    "source_url",
    "source_title",
    "subject",
    "grade",
    "topic",
    "language",
    "raw_text",
)


@dataclass
class NormalizationIssue:
    path: Path
    reasons: list[str]


def clean_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\xa0", " ")
    text = SPACE_RE.sub(" ", text)
    text = NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def infer_language(*texts: str) -> str:
    combined = "\n".join(text for text in texts if text)
    return "TH" if THAI_RE.search(combined) else "EN"


def slugify(text: Any, fallback: str = "document") -> str:
    slug = SLUG_RE.sub("-", clean_text(text).lower()).strip("-")
    return slug or fallback


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_source_name(value: Any) -> str:
    source = clean_text(value).lower()
    if "sci" in source and "math" in source:
        return "scimath"
    if "openstax" in source:
        return "openstax"
    return source or "unknown"


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items: list[str] = []
        for item in value:
            if isinstance(item, dict):
                text = clean_text(
                    item.get("text")
                    or item.get("content")
                    or item.get("value")
                    or item.get("term")
                    or " ".join(str(v) for v in item.values())
                )
            else:
                text = clean_text(item)
            if text:
                items.append(text)
        return list(dict.fromkeys(items))
    text = clean_text(value)
    return [text] if text else []


def normalize_sections(value: Any, raw_text: str) -> tuple[list[dict], bool]:
    repaired = False
    sections: list[dict] = []

    if isinstance(value, str):
        repaired = True
        text = clean_text(value)
        if text:
            sections.append({"heading": "Content", "text": text, "order": 1})
    elif isinstance(value, list):
        for idx, section in enumerate(value, start=1):
            if isinstance(section, dict):
                heading = clean_text(section.get("heading") or section.get("title") or "Content")
                text = clean_text(section.get("text") or section.get("content") or section.get("body"))
            else:
                heading = "Content"
                text = clean_text(section)
                repaired = True
            if text:
                sections.append({"heading": heading or "Content", "text": text, "order": idx})
    elif value:
        repaired = True

    if not sections and raw_text:
        repaired = True
        sections.append({"heading": "Content", "text": raw_text, "order": 1})

    return sections, repaired


def sections_to_raw_text(sections: Iterable[dict]) -> str:
    blocks: list[str] = []
    for section in sections:
        heading = clean_text(section.get("heading") or "Content")
        text = clean_text(section.get("text") or section.get("content") or "")
        if text:
            blocks.append(f"{heading}\n{text}" if heading else text)
    return clean_text("\n\n".join(blocks))


def validate_normalized_document(doc: dict) -> list[str]:
    reasons: list[str] = []
    if not isinstance(doc, dict):
        return ["normalized document must be a JSON object"]
    for field in REQUIRED_NORMALIZED_FIELDS:
        value = doc.get(field)
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"missing or empty required field: {field}")
    if doc.get("language") not in {"TH", "EN"}:
        reasons.append("language must be TH or EN")
    if not clean_text(doc.get("raw_text")):
        reasons.append("raw_text is empty")
    if not isinstance(doc.get("sections", []), list):
        reasons.append("sections must be a list")
    return reasons


class BaseDocumentNormalizer:
    source_name = "unknown"

    def normalize(self, raw: dict, path: Path | None = None) -> dict:
        repaired = False
        metadata = raw.get("metadata") if isinstance(raw.get("metadata"), dict) else {}

        source = normalize_source_name(raw.get("source") or self.source_name)
        source_url = clean_text(raw.get("source_url") or raw.get("url") or raw.get("link"))
        source_title = clean_text(raw.get("source_title") or raw.get("title") or raw.get("name"))
        subject = clean_text(raw.get("subject") or self._path_part(path, -3))
        grade = clean_text(raw.get("grade") or self._path_part(path, -2))
        topic = clean_text(raw.get("topic") or raw.get("category") or raw.get("breadcrumb") or source_title)
        subtopic = clean_text(raw.get("subtopic") or raw.get("lesson") or "")

        raw_text = clean_text(raw.get("raw_text") or raw.get("content") or raw.get("body") or raw.get("text"))
        sections, section_repaired = normalize_sections(raw.get("sections"), raw_text)
        repaired = repaired or section_repaired
        if not raw_text and sections:
            raw_text = sections_to_raw_text(sections)
            repaired = True

        language = clean_text(raw.get("language") or metadata.get("language")).upper()
        if language not in {"TH", "EN"}:
            language = infer_language(source_title, topic, raw_text)
            repaired = True

        if not source_title:
            source_title = topic or (path.stem if path else "Untitled")
            repaired = True
        if not topic:
            topic = source_title
            repaired = True

        original_topic = raw.get("topic")
        original_subtopic = raw.get("subtopic")
        topic = clean_text(topic).strip(" -_|")
        subtopic = clean_text(subtopic).strip(" -_|")

        doc_id_base = "_".join(
            slugify(part)
            for part in [source, subject, grade, topic, subtopic or source_title]
            if clean_text(part)
        )
        doc_hash = content_hash(raw_text)[:12] if raw_text else hashlib.sha1(str(path).encode()).hexdigest()[:12]

        normalized_metadata = {
            **metadata,
            "scraped_at": clean_text(raw.get("scraped_at") or metadata.get("scraped_at")),
            "scraper_version": clean_text(raw.get("scraper_version") or metadata.get("scraper_version") or "v1"),
            "content_hash": content_hash(raw_text) if raw_text else "",
            "normalization_status": "repaired" if repaired else "clean",
            "normalized_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if original_topic is not None and clean_text(original_topic) != topic:
            normalized_metadata["original_topic"] = clean_text(original_topic)
        if original_subtopic is not None and clean_text(original_subtopic) != subtopic:
            normalized_metadata["original_subtopic"] = clean_text(original_subtopic)

        return {
            "doc_id": clean_text(raw.get("doc_id")) or f"{doc_id_base}_{doc_hash}",
            "source": source,
            "source_url": source_url,
            "source_title": source_title,
            "subject": subject,
            "grade": grade,
            "topic": topic,
            "subtopic": subtopic,
            "language": language,
            "content_type": clean_text(raw.get("content_type") or "lesson"),
            "sections": sections,
            "key_terms": normalize_list(raw.get("key_terms")),
            "equations": normalize_list(raw.get("equations")),
            "examples": normalize_list(raw.get("examples")),
            "raw_text": raw_text,
            "metadata": normalized_metadata,
        }

    @staticmethod
    def _path_part(path: Path | None, offset: int) -> str:
        if path is None:
            return ""
        try:
            return path.parts[offset]
        except IndexError:
            return ""


class OpenStaxNormalizer(BaseDocumentNormalizer):
    source_name = "openstax"


class SciMathNormalizer(BaseDocumentNormalizer):
    source_name = "scimath"

    def normalize(self, raw: dict, path: Path | None = None) -> dict:
        doc = super().normalize(raw, path)
        doc["source"] = "scimath"
        doc["language"] = infer_language(doc["source_title"], doc["topic"], doc["raw_text"])
        return doc


def normalizer_for(raw: dict, path: Path | None = None) -> BaseDocumentNormalizer:
    source = normalize_source_name(raw.get("source"))
    path_text = str(path or "").lower()
    if source == "scimath" or "scimath" in path_text:
        return SciMathNormalizer()
    return OpenStaxNormalizer()


def normalized_output_path(raw_path: Path, normalized: dict, out_root: Path) -> Path:
    source = normalized.get("source") or "unknown"
    subject = normalized.get("subject") or "unknown"
    grade = normalized.get("grade") or "unknown"
    filename = f"{slugify(normalized.get('topic') or raw_path.stem)}.json"
    return out_root / source / subject / grade / filename


def normalize_file(raw_path: Path, out_root: Path = NORMALIZED_DIR) -> tuple[Path | None, list[str]]:
    try:
        with open(raw_path, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as exc:
        return None, [f"failed to read/parse JSON: {exc}"]

    if not isinstance(raw, dict):
        return None, ["raw page must be a JSON object"]

    normalized = normalizer_for(raw, raw_path).normalize(raw, raw_path)
    reasons = validate_normalized_document(normalized)
    if reasons:
        return None, reasons

    out_path = normalized_output_path(raw_path, normalized, out_root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    return out_path, []


def iter_raw_json_files(
    raw_root: Path = RAW_DIR,
    subjects: list[str] | None = None,
    grades: list[str] | None = None,
):
    for path in sorted(raw_root.rglob("*.json")):
        parts = set(path.parts)
        if subjects and not any(subject in parts for subject in subjects):
            continue
        if grades and not any(grade in parts for grade in grades):
            continue
        yield path


def normalize_all(
    subjects: list[str] | None = None,
    grades: list[str] | None = None,
    raw_root: Path = RAW_DIR,
    out_root: Path = NORMALIZED_DIR,
) -> dict:
    files = list(iter_raw_json_files(raw_root, subjects, grades))
    written: list[str] = []
    issues: list[NormalizationIssue] = []

    for path in files:
        out_path, reasons = normalize_file(path, out_root)
        if reasons:
            issues.append(NormalizationIssue(path=path, reasons=reasons))
            logger.warning(f"Skipping unnormalizable page {path}: {'; '.join(reasons)}")
        elif out_path:
            written.append(str(out_path))

    summary = {
        "total_files": len(files),
        "normalized_files": len(written),
        "invalid_files": len(issues),
        "written": written,
        "invalid_details": [
            {"path": str(issue.path), "reasons": issue.reasons}
            for issue in issues
        ],
    }
    logger.success(
        f"Normalization complete: {summary['normalized_files']} normalized | "
        f"{summary['invalid_files']} invalid | {summary['total_files']} total"
    )
    return summary


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Normalize scraped JSON files")
    p.add_argument("--subjects", nargs="*")
    p.add_argument("--grades", nargs="*")
    args = p.parse_args()
    print(json.dumps(normalize_all(args.subjects, args.grades), indent=2))
