# Tornado Requests
![](https://github.com/CeresCa/torn-requests/workflows/Python%20application/badge.svg)  
  
  
## 使用示例（Example）:
```python
import tornado.ioloop
from torn_requests import requests

async def http_request():
    client = requests.Requests()
    url = "http://httpbin.org/post"
    data = {"hello": "world"}
    rsp = await client.request(
        url, method="POST", to_json=data)
    print(rsp)
io_loop = tornado.ioloop.IOLoop.current()
io_loop.run_sync(http_request())

```