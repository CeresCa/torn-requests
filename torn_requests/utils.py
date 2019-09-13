import mimetypes


def encode_multipart_formdata(fields, files):
    """参考urllib，拼接multipart/form-data类型的HTTP请求中body，
       返回拼接的body内容及Content-Type"""
    boundary = "----------ThIs_Is_tHe_bouNdaRY_$"
    crlf = "\r\n"
    l = []
    for (key, value) in fields:
        l.append("--" + boundary)
        l.append('Content-Disposition: form-data; name="%s"' % key)
        l.append("")
        l.append(value)
    for (key, filename, value) in files:

        l.append("--" + boundary)
        l.append(
            'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename)
        )
        l.append("Content-Type: %s" % get_content_type(filename))
        l.append("")
        l.append(value)
    l.append("--" + boundary + "--")
    l.append("")
    body = crlf.join(l)
    content_type = "multipart/form-data; boundary=%s" % boundary
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def encoded_dict(in_dict):
    if not in_dict:
        return
    out_dict = {}
    for k, v in in_dict.items():
        if isinstance(v, str):
            v = v.encode("utf8")
        elif isinstance(v, bytes):
            # Must be encoded in UTF-8
            v.decode("utf8")
        out_dict[k] = v
    return out_dict
