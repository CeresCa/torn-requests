import unittest

import tornado.testing

from torn_requests import requests


class TestClient(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_get_method(self):
        client = requests.Requests()
        url = "http://z.cn"
        rsp = yield client.request(url)
        self.assertEqual(rsp.code, 200)

    @tornado.testing.gen_test
    def test_post_method(self):
        client = requests.Requests()
        url = "http://httpbin.org/post"
        data = {"hello": "world"}
        rsp = yield client.request(url, method="POST", to_json=data)
        print(rsp.body)
        self.assertIn("world", str(rsp.body))

    @tornado.testing.gen_test
    def test_post_method_upload_file(self):
        client = requests.Requests()
        url = "http://httpbin.org/post"
        files = files = [("fieldname", "filename", "SomeTextForTextFile\r\n")]
        rsp = yield client.upload_file("https://httpbin.org/post", files)
        print(rsp.body)
        self.assertIn("SomeTextForTextFile", str(rsp.body))


if __name__ == "__main__":
    unittest.main()
