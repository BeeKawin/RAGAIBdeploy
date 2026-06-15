import unittest

from fastapi.testclient import TestClient

from chat.api import app
from config.settings import BASE_DIR


class TestDemoSite(unittest.TestCase):
    def test_demo_homepage_serves_static_html(self):
        client = TestClient(app)
        response = client.get("/demo/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Live RAG vs Baseline Evaluation", response.text)
        self.assertIn("API Base URL", response.text)
        self.assertIn("./config.js", response.text)
        self.assertIn("./app.js", response.text)

    def test_demo_app_formats_latex_math_tokens(self):
        app_js = (BASE_DIR / "demo" / "app.js").read_text(encoding="utf-8")

        self.assertIn("function formatFormula", app_js)
        self.assertIn("∑", app_js)
        self.assertIn("formatAnswerHtml", app_js)
        self.assertIn("innerHTML = formatAnswerHtml", app_js)


if __name__ == "__main__":
    unittest.main()
