import unittest
from unittest.mock import patch

from langchain_core.documents import Document

from retrieval import rag_chain
from retrieval.rag_chain import EduRAGChain, _preferred_source, _target_answer_type, _target_language
from vector_store.indexer import VectorStoreManager


class FakeVectorStore:
    def __init__(self):
        self.calls = []

    def search(self, query, subject=None, grade=None, source=None, top_k=6):
        self.calls.append(
            {
                "query": query,
                "subject": subject,
                "grade": grade,
                "source": source,
                "top_k": top_k,
            }
        )
        if source == "openstax":
            return [
                Document(
                    page_content="openstax result",
                    metadata={"chunk_id": "openstax-1", "source": "openstax"},
                )
            ]
        return [
            Document(
                page_content="openstax result",
                metadata={"chunk_id": "openstax-1", "source": "openstax"},
            ),
            Document(
                page_content="scimath result",
                metadata={"chunk_id": "scimath-1", "source": "scimath"},
            ),
        ]


class GradeFallbackVectorStore:
    def __init__(self):
        self.calls = []

    def search(self, query, subject=None, grade=None, source=None, top_k=6):
        self.calls.append({"grade": grade, "source": source})
        if grade == "M5":
            return []
        if grade is None and source == "openstax":
            return [
                Document(
                    page_content="cross-grade result",
                    metadata={"chunk_id": "m6-circuit", "source": "openstax", "grade": "M6"},
                )
            ]
        return []


class FakeCollection:
    def count(self):
        return 12


class FakeChromaClient:
    def get_or_create_collection(self, name, metadata):
        self.name = name
        self.metadata = metadata
        return FakeCollection()


class TestSourceRouting(unittest.TestCase):
    def test_preferred_source_from_language_and_query(self):
        self.assertEqual(_preferred_source("What is force?", language="EN"), "openstax")
        self.assertEqual(_preferred_source("แรงคืออะไร", language=None), "scimath")
        self.assertEqual(_preferred_source("What is force?", source="scimath"), "scimath")

    def test_retrieve_falls_back_when_preferred_source_is_sparse(self):
        chain = EduRAGChain.__new__(EduRAGChain)
        chain.vsm = FakeVectorStore()

        docs = chain._retrieve("What is force?", language="EN", top_k=6, min_source_results=2)

        self.assertEqual([doc.metadata["chunk_id"] for doc in docs], ["openstax-1", "scimath-1"])
        self.assertEqual(chain.vsm.calls[0]["source"], "openstax")
        self.assertIsNone(chain.vsm.calls[1]["source"])

    def test_target_answer_type_defaults_invalid_values_to_general(self):
        self.assertEqual(_target_answer_type("homework-help"), "homework-help")
        self.assertEqual(_target_answer_type(" HOMEWORK-HELP "), "homework-help")
        self.assertEqual(_target_answer_type("calculation"), "general")
        self.assertEqual(_target_answer_type(None), "general")

    def test_target_language_uses_exact_prompt_tokens(self):
        self.assertEqual(_target_language("EN"), "EN")
        self.assertEqual(_target_language(" english "), "EN")
        self.assertEqual(_target_language("TH"), "TH")
        self.assertEqual(_target_language("thai"), "TH")
        self.assertEqual(_target_language(None), "Match the user question language")

    def test_retrieve_uses_soft_grade_fallback(self):
        chain = EduRAGChain.__new__(EduRAGChain)
        chain.vsm = GradeFallbackVectorStore()

        docs = chain._retrieve("Explain Ohm's law", subject="physics", grade="M5", language="EN")

        self.assertEqual([doc.metadata["chunk_id"] for doc in docs], ["m6-circuit"])
        self.assertIn({"grade": None, "source": "openstax"}, chain.vsm.calls)

    def test_vector_where_accepts_source_filter(self):
        vsm = VectorStoreManager.__new__(VectorStoreManager)
        where = vsm._build_where(subject="physics", grade="M4", source="openstax")

        self.assertEqual(
            where,
            {
                "$and": [
                    {"subject": {"$eq": "physics"}},
                    {"grade": {"$eq": "M4"}},
                    {"source": {"$eq": "openstax"}},
                ]
            },
        )

    def test_vector_stats_does_not_load_embedding_model(self):
        vsm = VectorStoreManager.__new__(VectorStoreManager)
        vsm.embedder = None
        vsm._client = FakeChromaClient()
        vsm._store = None

        stats = vsm.stats()

        self.assertEqual(stats["total_chunks"], 12)
        self.assertFalse(stats["embedding_loaded"])
        self.assertIsNone(vsm.embedder)

    def test_rag_chain_constructor_does_not_create_llm(self):
        with patch.object(rag_chain, "get_vector_store", return_value=FakeVectorStore()):
            with patch.object(rag_chain, "_get_llm", side_effect=AssertionError("LLM loaded at startup")):
                chain = EduRAGChain()

        self.assertIsInstance(chain.vsm, FakeVectorStore)


if __name__ == "__main__":
    unittest.main()
