#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import logging
import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.web
from urllib import urllib


def encode_multipart_formdata(fields, files):
    '''拼接multipart/form-data类型的HTTP请求中body，
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
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


class HttpclientUtil(object):

    def req(self, url, method='GET', params=None, data=None, json_=None, headers=None, body_=None):
        http_client = tornado.httpclient.AsyncHTTPClient(max_clients=5000)
        query_string = urllib.urlencode(encoded_dict(params))
        url = u'{url}?{query_string}'.format(
            url=url, query_string=query_string)
        logging.info(u'请求的url {}: {}, headers {}'.format(method, url, headers))

        if method in ('GET', 'DELETE'):
            request = tornado.httpclient.HTTPRequest(url=url,
                                                     method=method,
                                                     validate_cert=False,
                                                     headers=headers,
                                                     request_timeout=3.0,
                                                     connect_timeout=3.0)
            return http_client.fetch(request)
        elif method in ('POST', 'PUT'):
            if data:
                data = encoded_dict(data)
                body = urllib.urlencode(data)
            else:
                body = json.dumps(json_)
            if body_:
                body = body_
            request = tornado.httpclient.HTTPRequest(url=url,
                                                     method=method,
                                                     body=body,
                                                     validate_cert=False,
                                                     headers=headers,
                                                     request_timeout=3.0,
                                                     connect_timeout=3.0)
            return http_client.fetch(request)
        else:
            return

    def upload_file(self, url, file_):
        '''上传文件'''
        files = [('file', 'upload', file_)]
        fields = tuple()
        content_type, body = encode_multipart_formdata(fields, files)
        headers = {"Content-Type": content_type,
                   'content-length': str(len(body))
                   }
        return self.req(url=url, method='POST', params={}, headers=headers, body_=body)
