# pylint: disable=too-few-public-methods,no-self-use,unused-argument
from aiohttp import web
from aiohttp.test_utils import make_mocked_coro
from hntm.proxy import handle
from hntm.utils import trademarkify_page_html

with open("tests/fixtures/home_before.html", encoding="utf-8") as before_fp:
    home_before_html = before_fp.read()

with open("tests/fixtures/home_after.html", encoding="utf-8") as after_fp:
    home_after_html = after_fp.read()


def make_client_session_stub(status_, content_type_, headers_, text_coro, read_coro):
    class ClientResponseStub:
        status = status_
        content_type = content_type_
        headers = headers_
        text = text_coro
        read = read_coro

    class RequestContextManagerStub:
        async def __aenter__(self):
            return ClientResponseStub()

        async def __aexit__(self, exc_type, exc_value, traceback):
            pass

    class ClientSessionStub:
        def get(self, url):
            return RequestContextManagerStub()

    return ClientSessionStub()


async def persistent_session(web_app):
    web_app["PERSISTENT_SESSION"] = make_client_session_stub(
        status_=200,
        content_type_="text/html",
        headers_={"content-type": "text/html"},
        text_coro=make_mocked_coro(home_before_html),
        read_coro=make_mocked_coro(None),
    )
    yield


async def test_server(aiohttp_client):  # pylint: disable=redefined-outer-name
    app = web.Application()
    app.add_routes([web.get(r"/{path:.*}", handle)])
    app.cleanup_ctx.append(persistent_session)
    client = await aiohttp_client(app)
    resp = await client.get("/")
    assert resp.status == 200
    home_html = await resp.text()
    assert trademarkify_page_html(home_html) == home_after_html
