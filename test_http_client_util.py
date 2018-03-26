import unittest
import httpclient_util
import tornado.testing


class TestClient(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_get_method(self):
        client = httpclient_util.HttpclientUtil()
        url = 'http://z.cn'
        rsp = yield client.req(url)
        self.assertEqual(rsp.code, 200)

    @tornado.testing.gen_test
    def test_post_method(self):
        client = httpclient_util.HttpclientUtil()
        url = 'http://httpbin.org/post'
        data = {'hello': 'world'}
        rsp = yield client.req(url, method='POST', json_data=data)
        print(rsp.body)
        self.assertIn('world', str(rsp.body))
