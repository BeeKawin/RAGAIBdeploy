import unittest

from evaluation.retrieval_eval import _preferred_source_for_language
from evaluation.topic_aliases import canonicalize, terms_match


class TestTopicAliases(unittest.TestCase):
    def test_english_and_thai_topic_aliases_match(self):
        self.assertEqual(canonicalize("Momentum and Collisions"), canonicalize("โมเมนตัมและการชน"))
        self.assertEqual(canonicalize("Kinematics 1D"), canonicalize("การเคลื่อนที่แนวตรง"))
        self.assertEqual(canonicalize("สภาพสมดุล (Equilibrium)"), canonicalize("สมดุลกล"))
        self.assertEqual(canonicalize("ฟิสิกส์อะตอม (Atomic Physics)"), canonicalize("ฟิสิกส์อะตอม"))

    def test_terms_match_keeps_literal_fallback(self):
        self.assertTrue(
            terms_match(
                {"measurement"},
                {"Measurement and Units", "Introduction"},
            )
        )

    def test_language_selects_preferred_source(self):
        self.assertEqual(_preferred_source_for_language("EN"), "openstax")
        self.assertEqual(_preferred_source_for_language("TH"), "scimath")
        self.assertIsNone(_preferred_source_for_language(""))


if __name__ == "__main__":
    unittest.main()
