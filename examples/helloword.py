import tornado.ioloop

from torn_requests.requests import Requests


async def main():
    get_url = "http://httpbin.org/get"
    requests = Requests()
    get_rsp = await requests.request(
        get_url,
        method="GET",
        params={"foor": "bar", "好": "👌"},
        connect_timeout=5,
        request_timeout=10,
    )
    print(get_rsp)
    print(get_rsp.headers)
    print(get_rsp.body)

    post_url = "http://httpbin.org/post"
    post_rsp = await requests.request(
        post_url,
        method="POST",
        to_json={"foor": "bar", "好": "👌"},
        connect_timeout=10,
        request_timeout=10,
    )
    print(post_rsp)
    print(post_rsp.headers)
    print(post_rsp.body)


if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(main)
