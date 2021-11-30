from aiohttp import ClientError, ClientSession, web

from .utils import HN_HTTPS, HOST, PORT, trademarkify_page_html


async def handle(request):
    session = request.app["PERSISTENT_SESSION"]
    try:
        async with session.get(f"{HN_HTTPS}{request.path_qs}") as r:
            if (r.status != 200) or (r.content_type != "text/html"):
                return web.Response(
                    body=await r.read(),
                    content_type=r.headers["content-type"],
                    status=r.status,
                )

            html = await r.text()
            trademarkified_html = trademarkify_page_html(html)
            return web.Response(text=trademarkified_html, content_type="text/html")

    except ClientError as e:
        return web.Response(
            text=f"<b>Request error</b><br>{e}",
            content_type="text/html",
            status=500,
        )


async def persistent_session(web_app):
    web_app["PERSISTENT_SESSION"] = session = ClientSession()
    yield
    await session.close()


app = web.Application()
app.add_routes([web.get(r"/{path:.*}", handle)])
app.cleanup_ctx.append(persistent_session)

if __name__ == "__main__":
    web.run_app(app, host=HOST, port=PORT)
