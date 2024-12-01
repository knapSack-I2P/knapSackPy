import json
from aiohttp import web
from aiohttp_socks import ProxyConnector

from shared.knapsack import knapsack
from misc import server_print as print

def serverside():
    async def handle_default(request):
        return web.HTTPFound(location='/ping')

    async def handle_ping(request):
        print(request)
        print(knapsack.serialize())
        return web.Response(body=json.dumps(knapsack.serialize()), content_type='')

    async def handle_m3u8(request):
        print(request)
        print(knapsack.serialize())
        return web.FileResponse("vids/meme/meme0.ts", 1024*40)

    app = web.Application()
    app.router.add_get('/', handle_default)
    app.router.add_get('/ping', handle_ping)
    app.router.add_get('/m3u8', handle_m3u8)

    connector = ProxyConnector.from_url('socks5://localhost:4444')  # SOCKS5 прокси I2P
    app['connector'] = connector
    return app
