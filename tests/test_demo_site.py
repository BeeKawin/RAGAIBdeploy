import unittest

from fastapi.testclient import TestClient

from chat.api import app


class TestDemoSite(unittest.TestCase):
    def test_demo_homepage_serves_static_html(self):
        client = TestClient(app)
        response = client.get("/demo/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Live RAG vs Baseline Evaluation", response.text)
        self.assertIn("API Base URL", response.text)
        self.assertIn("./config.js", response.text)
        self.assertIn("./app.js", response.text)


if __name__ == "__main__":
    unittest.main()
