import unittest

from scraper.scimath_scraper import parse_html


class TestScimathScraper(unittest.TestCase):
    def test_parse_html_extracts_expected_fields(self):
        html = """
        <html>
            <body>
                <h2>บทนำ</h2>
                <p>นี่คือเนื้อหาทดสอบ</p>
                <h2>คำสำคัญ</h2>
                <ul>
                    <li>อะตอม</li>
                    <li>โมเลกุล</li>
                </ul>
                <h2>ตัวอย่าง</h2>
                <p>ตัวอย่างการคำนวณมวลอะตอม</p>
            </body>
        </html>
        """

        page = parse_html(
            html,
            subject="chemistry",
            grade="M4",
            topic="Atomic Model",
            url="https://www.scimath.org/lesson-chemistry/item/7121-atomic-model",
        )

        self.assertEqual(page.subject, "chemistry")
        self.assertEqual(page.grade, "M4")
        self.assertEqual(page.topic, "Atomic Model")
        self.assertEqual(page.source, "SciMath")
        self.assertIn("อะตอม", page.key_terms)
        self.assertIn("โมเลกุล", page.key_terms)
        self.assertTrue(any("ตัวอย่าง" in content for content in page.examples))
        self.assertTrue(page.raw_text.startswith("บทนำ"))
