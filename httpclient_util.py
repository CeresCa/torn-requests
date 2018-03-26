import json
import logging
import pprint
import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.web
from urllib import parse as urllib


def encode_multipart_formdata(fields, files):
    '''参考urllib，拼接multipart/form-data类型的HTTP请求中body，
       返回拼接的body内容及Content-Type'''
    boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
    crlf = '\r\n'
    l = []
    for (key, value) in fields:
        l.append('--' + boundary)
        l.append('Content-Disposition: form-data; name="%s"' % key)
        l.append('')
        l.append(value)
    for (key, filename, value) in files:
        filename = filename.encode("utf8")
        l.append('--' + boundary)
        l.append(
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                key, filename
            )
        )
        l.append('Content-Type: %s' % get_content_type(filename))
        l.append('')
        l.append(value)
    l.append('--' + boundary + '--')
    l.append('')
    body = crlf.join(l)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body


def get_content_type(filename):
    import mimetypes
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def encoded_dict(in_dict):
    if not in_dict:
        return
    out_dict = {}
    for k, v in in_dict.items():
        if isinstance(v, str):
            v = v.encode('utf8')
        elif isinstance(v, bytes):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


class HttpclientUtil(object):

    def req(self, url, method='GET', params=None, form_data=None, json_data=None, raw_body=None, headers=None):
        http_client = tornado.httpclient.AsyncHTTPClient(max_clients=5000)
        if params:
            query_string = urllib.urlencode(encoded_dict(params))
        else:
            query_string = ''
        url = u'{url}?{query_string}'.format(
            url=url, query_string=query_string)
        logging.info(u'请求的url {}: {}, headers {}'.format(method, url, headers))
        if not headers:
            headers = {}
        if method in ('GET', 'DELETE'):
            body = None
        elif method in ('POST', 'PUT'):
            if raw_body:
                body = raw_body
            elif form_data:
                form_data = encoded_dict(form_data)
                body = urllib.urlencode(form_data)
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            else:
                body = json.dumps(json_data)
                headers['Content-Type'] = 'application/json'

        request = tornado.httpclient.HTTPRequest(url=url,
                                                 method=method,
                                                 body=body,
                                                 validate_cert=False,
                                                 headers=headers,
                                                 request_timeout=10.0,
                                                 connect_timeout=10.0)
        return http_client.fetch(request)

    def upload_file(self, url, file_):
        '''使用tornado AsyncHttpClient异步上传文件'''
        files = [('file', 'upload', file_)]
        fields = tuple()
        content_type, body = encode_multipart_formdata(fields, files)
        headers = {"Content-Type": content_type,
                   'content-length': str(len(body))
                   }
        return self.req(url=url, method='POST', params={}, headers=headers, raw_body=body)


async def main():
    get_url = 'http://httpbin.org/get'
    http_client = HttpclientUtil()
    get_rsp = await http_client.req(get_url, method='GET', params={'foor': 'bar', '好': '👌'})
    if not get_rsp.error:
        pprint.pprint(get_rsp.body)
    else:
        print(get_rsp)

    post_url = 'http://httpbin.org/post'
    post_rsp = await http_client.req(post_url, method='POST', json_data={'foor': 'bar', '好': '👌'})
    if not post_rsp.error:
        pprint.pprint(post_rsp.body)
    else:
        print(post_rsp)

if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(main)
