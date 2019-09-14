import json
import logging
from urllib import parse as urllib

import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.web

from torn_requests.utils import encode_multipart_formdata, encoded_dict


class Requests(object):
    def __init__(self, max_clients=1000):
        self.httpclient = tornado.httpclient.AsyncHTTPClient(max_clients)

    def request(
        self,
        url=None,
        method="GET",
        params=None,
        to_urlencode=None,
        to_json=None,
        raw_body=None,
        headers=None,
        raw_request=None,
        request_timeout=3.0,
        connect_timeout=3.0,
    ):
        """
        包装tornado httpclient，简化网络请求参数
        Args:
            url (unicode): 链接地址
            method (str): 请求方法
            params (dict): url参数
            to_urlencode (dict): x-www-form-urlencoded body 参数
            to_json (dict): json body 参数
            headers (dict): headers
            raw_body (unicode): 原始body字符串
            raw_request (tornado.httpclient.HTTPRequest()): 自定义request
        """

        if not raw_request:
            if params:
                query_string = urllib.urlencode(encoded_dict(params))
                url = u"{url}?{query_string}".format(url=url, query_string=query_string)

            if method in ("GET", "DELETE", "HEAD"):
                body = None
            elif method in ("POST", "PUT", "PATCH"):
                if to_urlencode:
                    to_urlencode = encoded_dict(to_urlencode)
                    body = urllib.urlencode(to_urlencode)
                else:
                    body = json.dumps(to_json)
                if raw_body:
                    body = raw_body
            else:
                body = None
            request = tornado.httpclient.HTTPRequest(
                url=url,
                method=method,
                body=body,
                validate_cert=False,
                headers=headers,
                request_timeout=request_timeout,
                connect_timeout=connect_timeout,
            )
        else:
            request = raw_request
        logging.info(
            u"请求的url {}: {}, headers {}".format(
                request.method, request.url, request.headers
            )
        )
        return self.httpclient.fetch(request)

    def upload_file(self, url, files, connect_timeout=60, request_timeout=60):
        """使用tornado AsyncHttpClient异步上传文件
           files = [("fieldname", "filename", file_body)]
        """
        fields = tuple()
        content_type, body = encode_multipart_formdata(fields, files)
        headers = {"Content-Type": content_type, "content-length": str(len(body))}
        return self.request(
            url=url,
            method="POST",
            params={},
            headers=headers,
            raw_body=body,
            connect_timeout=connect_timeout,
            request_timeout=request_timeout,
        )
