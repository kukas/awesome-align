import json
import unittest
from flask import Flask
from align_server import create_aligner


class DummyAligner:
    def align(self, lines, batch_size=None):
        all_results = []
        for line in lines:
            src_tokens, trg_tokens = line.split(" ||| ")
            src_tokens = src_tokens.split()
            trg_tokens = trg_tokens.split()
            res = [(i, i) for i in range(min(len(src_tokens), len(trg_tokens)))]
            all_results.append(res)
        return all_results


class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        app = create_aligner({"TESTING": True, "aligner": DummyAligner()})
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_info_route(self):
        response = self.client.get("/info")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Word alignment server", response.data)

    def test_align_with_single_sentence(self):
        payload = {
            "src_text": "This is a test sentence.",
            "trg_text": "Ceci est une phrase de test.",
        }
        response = self.client.post("/align/en-fr", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("alignment", data)
        # check the expected dummy output
        self.assertListEqual(
            data["alignment"], [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
        )
        self.assertIn("src_tokens", data)
        expected_src_tokens = ["This", "is", "a", "test", "sentence", "."]
        self.assertListEqual(data["src_tokens"], expected_src_tokens)
        self.assertIn("trg_tokens", data)
        expected_trg_tokens = ["Ceci", "est", "une", "phrase", "de", "test", "."]
        self.assertListEqual(data["trg_tokens"], expected_trg_tokens)

    def test_align_with_batch_sentence(self):
        N = 20
        payload = {
            "src_text": ["This is a test sentence."] * N,
            "trg_text": ["Ceci est une phrase de test."] * N,
        }
        response = self.client.post("/align/en-fr", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertEqual(len(data["alignment"]), N)
        self.assertIn("src_tokens", data)
        expected_src_tokens = ["This", "is", "a", "test", "sentence", "."]
        self.assertListEqual(data["src_tokens"][0], expected_src_tokens)
        self.assertIn("trg_tokens", data)

    def test_align_with_batch_tokenized_sentences(self):
        N = 20
        payload = {
            "src_tokens": [["hello", "world"]]*N,
            "trg_tokens": [["hola", "mundo"]]*N,
        }
        response = self.client.post("/align/en-es", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertEqual(len(data["alignment"]), N)
        self.assertIn("src_tokens", data)
        self.assertListEqual(data["src_tokens"][0], payload["src_tokens"][0])
        self.assertIn("trg_tokens", data)
        self.assertListEqual(data["trg_tokens"][0], payload["trg_tokens"][0])

    def test_align_with_single_tokenized_sentence(self):
        payload = {"src_tokens": ["he-llo", "wor-ld"], "trg_tokens": ["hola", "mundo"]}
        response = self.client.post("/align/en-es", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("alignment", data)
        self.assertListEqual(data["alignment"], [[0, 0], [0, 1]])
        self.assertIn("src_tokens", data)
        self.assertListEqual(data["src_tokens"], payload["src_tokens"])
        self.assertIn("trg_tokens", data)
        self.assertListEqual(data["trg_tokens"], payload["trg_tokens"])

    def test_align_with_invalid_language_pair(self):
        payload = {
            "src_text": "This is a test sentence.",
            "trg_text": "Ceci est une phrase de test.",
        }
        response = self.client.post("/align/invalid-lang", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_align_with_invalid_request_format(self):
        payload = {"invalid_key": "This is an invalid request format."}
        response = self.client.post("/align/en-fr", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_align_with_empty_sentence(self):
        payload = {"src_tokens": [], "trg_tokens": []}
        response = self.client.post("/align/en-es", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"alignment":[],"src_tokens":[],"trg_tokens":[]})
        payload = {"src_tokens": "", "trg_tokens": "fefefe"}
        response = self.client.post("/align/en-es", json=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
