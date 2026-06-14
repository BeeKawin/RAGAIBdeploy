#!/usr/bin/env python3
"""Test that retrieval_eval works with the updated dataset."""

from evaluation.retrieval_eval import _load_rows, _expected_terms, _normalize_subject
from evaluation.eval_config import GOLD_QA_PATH
from collections import Counter

rows = _load_rows(GOLD_QA_PATH)
print(f"✓ Loaded {len(rows)} gold QA entries\n")

# Verify structure
print("Sample entries:")
for row in rows[:3]:
    print(f"  {row.get('id')}: {row.get('subject')}/{row.get('grade')}")
    print(f"    Q: {row.get('question')[:50]}...")
    print(f"    Expected terms: {_expected_terms(row)}")
    print()

# Check subject normalization
print("Subject normalization:")
subjects = set(row.get("subject", "").lower() for row in rows)
for subj in sorted(subjects):
    normalized = _normalize_subject(subj)
    count = sum(1 for r in rows if r.get("subject", "").lower() == subj)
    print(f"  {subj} -> {normalized}: {count} entries")

print()

# Check coverage
by_sg = Counter()
for row in rows:
    key = (row.get("subject", "").lower(), row.get("grade", ""))
    by_sg[key] += 1

print("Coverage by subject & grade:")
for key in sorted(by_sg.keys()):
    subj, grade = key
    print(f"  {subj:12} {grade:3}: {by_sg[key]:2} entries")

print(f"\nTotal: {len(rows)} entries")
print(f"Ready for retrieval evaluation!")
