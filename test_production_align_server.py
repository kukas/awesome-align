import json
import unittest
import requests
from pprint import pprint

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:8080"

    def test_index_route(self):
        r = requests.get(self.url)
        self.assertEqual(r.status_code, 200)
        # self.assertEqual(r.headers.get("Access-Control-Allow-Origin", ""), "*")

    def test_align_with_single_sentence(self):
        payload = {
            "src_text": "This is a test sentence.",
            "trg_text": "Ceci est une phrase de test.",
        }
        response = requests.post(self.url + "/align/en-fr", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertIn("src_tokens", data)
        expected_src_tokens = ["This", "is", "a", "test", "sentence", "."]
        self.assertListEqual(data["src_tokens"], expected_src_tokens)
        self.assertIn("trg_tokens", data)

    def test_align_with_too_large_request(self):
        N = 300 # 200 still works for 200kB request limit
        payload = {
            "src_text": ["^"*500] * N,
            "trg_text": ["^"*500] * N,
        }
        response = requests.post(self.url + "/align/en-fr", json=payload)
        # breakpoint()
        if response.status_code == 200:
            data = response.json()
            print(data)
        self.assertEqual(response.status_code, 413)

    def test_align_with_too_long_line(self):
        payload = {
            "src_text": "&"*600,
            "trg_text": "^"*600,
        }
        response = requests.post(self.url + "/align/en-fr", json=payload)
        self.assertEqual(response.status_code, 200)
    def test_unknown_token(self):
        payload = {
                "src_tokens": ['·'],
                "trg_tokens": ['·']
        }
        response = requests.post(self.url + "/align/cs-uk", json=payload)
        self.assertEqual(response.status_code, 200)
    def test_empty_tokens(self):
        payload = {
                "src_tokens": ['ahoj'],
                "trg_tokens": []
        }
        response = requests.post(self.url + "/align/cs-uk", json=payload)
        print(response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertListEqual(data["alignment"], [])
        self.assertIn("src_tokens", data)
        expected_src_tokens = ['ahoj']
        self.assertListEqual(data["src_tokens"], expected_src_tokens)
        self.assertIn("trg_tokens", data)
        expected_trg_tokens = []
        self.assertListEqual(data["trg_tokens"], expected_trg_tokens)
    def test_empty_text(self):
        payload = {
                "src_text": "",
                "trg_text": "hello"
        }
        response = requests.post(self.url + "/align/cs-uk", json=payload)
        print(response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertListEqual(data["alignment"], [])
        self.assertIn("src_tokens", data)
        expected_src_tokens = []
        self.assertListEqual(data["src_tokens"], expected_src_tokens)
        self.assertIn("trg_tokens", data)
        expected_trg_tokens = ["hello"]
        self.assertListEqual(data["trg_tokens"], expected_trg_tokens)
    def test_empty_tokens_batch(self):
        payload = {
                "src_tokens": [['ahoj'], ['ahoj'], [""]],
                "trg_tokens": [["hello"], [], ["hello"]]
        }
        response = requests.post(self.url + "/align/cs-uk", json=payload)
        print(response.text)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("alignment", data)
        self.assertIsInstance(data["alignment"], list)
        self.assertListEqual(data["alignment"], [[[0,0]],[],[]])



if __name__ == "__main__":
    unittest.main()
