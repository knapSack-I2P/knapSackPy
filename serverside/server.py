import functools
import json

from aiohttp import web
from aiohttp_socks import ProxyConnector

from constants import *
from shared.prettyIO import server_print as print
from shared.knapsack import knapsack


def block_clearnet(method):
    async def block(request):
        return web.HTTPProxyAuthenticationRequired()

    @functools.wraps(method)
    async def wrapper(request):
        if request.remote == '127.0.0.1':
            return await method(request)
        else:
            print(SERVER_CLEARNET_WARN)
            return await block(request)

    return wrapper


def serverside():
    @block_clearnet
    async def handle_default(request):
        print(request, expand_all=True)
        return web.HTTPFound(location='/ping')

    @block_clearnet
    async def handle_ping(request):
        return web.Response(body=json.dumps(knapsack.serialize()), content_type='')

    @block_clearnet
    async def handle_m3u8(request):
        return web.FileResponse("vids/meme/meme0.ts", 1024 * 40)

    app = web.Application()
    app.router.add_get('/', handle_default)
    app.router.add_get('/ping', handle_ping)
    app.router.add_get('/m3u8', handle_m3u8)

    connector = ProxyConnector.from_url(
        'socks5://localhost:4444')  # SOCKS5 прокси I2P
    app['connector'] = connector
    return app
