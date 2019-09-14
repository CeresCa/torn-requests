# Tornado Requests
![](https://github.com/CeresCa/torn-requests/workflows/Python%20application/badge.svg)  
  
  
## 使用示例（Example）:
```python
from torn_requests import requests

def http_request():
    client = requests.Requests()
    url = "http://httpbin.org/post"
    data = {"hello": "world"}
    rsp = yield client.request(
        url, method="POST", to_json=data)
    print(rsp)
```