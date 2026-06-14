import tempfile
import unittest
from pathlib import Path

from embeddings.document_normalizer import (
    OpenStaxNormalizer,
    SciMathNormalizer,
    normalize_file,
    validate_normalized_document,
)
from embeddings.document_processor import DocumentProcessor


class TestDocumentNormalizer(unittest.TestCase):
    def test_openstax_repairs_old_aliases_and_section_content(self):
        raw = {
            "subject": "physics",
            "grade": "M6",
            "topic": "Heat Transfer",
            "url": "https://openstax.org/books/physics/pages/heat-transfer",
            "title": "Heat Transfer",
            "sections": [
                {
                    "heading": "Conduction",
                    "content": "Conduction transfers thermal energy through direct particle collisions.",
                }
            ],
            "raw_text": "",
        }

        doc = OpenStaxNormalizer().normalize(raw)

        self.assertEqual(validate_normalized_document(doc), [])
        self.assertEqual(doc["source_url"], raw["url"])
        self.assertEqual(doc["source_title"], raw["title"])
        self.assertEqual(doc["sections"][0]["text"], raw["sections"][0]["content"])
        self.assertEqual(doc["metadata"]["normalization_status"], "repaired")

    def test_scimath_infers_thai_language(self):
        raw = {
            "subject": "chemistry",
            "grade": "M4",
            "topic": "Atomic Model",
            "url": "https://www.scimath.org/item/atomic-model",
            "title": "แบบจำลองอะตอม",
            "sections": "อะตอมเป็นหน่วยพื้นฐานของสสาร",
        }

        doc = SciMathNormalizer().normalize(raw)

        self.assertEqual(validate_normalized_document(doc), [])
        self.assertEqual(doc["source"], "scimath")
        self.assertEqual(doc["language"], "TH")
        self.assertEqual(doc["sections"][0]["heading"], "Content")

    def test_normalize_file_rejects_empty_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "empty.json"
            raw_path.write_text(
                '{"subject":"physics","grade":"M4","topic":"Bad","url":"local://bad","title":"Bad"}',
                encoding="utf-8",
            )

            out_path, reasons = normalize_file(raw_path, out_root=Path(tmp) / "normalized")

        self.assertIsNone(out_path)
        self.assertTrue(any("raw_text" in reason for reason in reasons))

    def test_processor_uses_normalized_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page_dir = root / "openstax" / "physics" / "M4"
            page_dir.mkdir(parents=True)
            page = page_dir / "newton.json"
            page.write_text(
                """
                {
                  "doc_id": "openstax_physics_m4_newton",
                  "source": "openstax",
                  "source_url": "local://newton",
                  "source_title": "Newton's Law",
                  "subject": "physics",
                  "grade": "M4",
                  "topic": "Newton's Law",
                  "subtopic": "Force",
                  "language": "EN",
                  "content_type": "lesson",
                  "sections": [
                    {
                      "heading": "Core idea",
                      "text": "Newton's second law explains that net force equals mass times acceleration in a system."
                    }
                  ],
                  "key_terms": [],
                  "equations": ["F = ma"],
                  "examples": [],
                  "raw_text": "Newton's second law explains that net force equals mass times acceleration in a system.",
                  "metadata": {
                    "content_hash": "abc123",
                    "normalization_status": "clean"
                  }
                }
                """,
                encoding="utf-8",
            )

            docs = DocumentProcessor().process_all(subjects=["physics"], grades=["M4"], root_dir=root)

        self.assertGreaterEqual(len(docs), 1)
        self.assertEqual(docs[0].metadata["doc_id"], "openstax_physics_m4_newton")
        self.assertIn("chunk_id", docs[0].metadata)
        self.assertEqual(docs[0].metadata["source_url"], "local://newton")
        self.assertEqual(docs[0].metadata["language"], "EN")
        self.assertEqual(docs[0].metadata["content_hash"], "abc123")


if __name__ == "__main__":
    unittest.main()
