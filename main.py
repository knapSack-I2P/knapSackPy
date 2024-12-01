import asyncio
import json

import aiohttp
from aiohttp import web
from aiohttp_socks import ProxyConnector

from knapclasses import KnapSack

DEST = "http://hr4zbelmgfioktfgrah6a6a2o7gsfgsq7wbxscll3kf2okpqgvga.b32.i2p/"
# DEST = "http://127.0.0.1:6626"


saved_videos: KnapSack = KnapSack()


def serverside():
    async def handle_default(request):
        return web.HTTPFound(location='/ping')

    async def handle_ping(request):
        print(request)
        print(saved_videos.serialize())
        return web.Response(body=json.dumps(saved_videos.serialize()), content_type='')

    async def handle_m3u8(request):
        print(request)
        print(saved_videos.serialize())
        return web.FileResponse("vids/meme/meme0.ts", 1024*40)

    app = web.Application()
    app.router.add_get('/', handle_default)
    app.router.add_get('/ping', handle_ping)
    app.router.add_get('/m3u8', handle_m3u8)

    connector = ProxyConnector.from_url(
        'socks5://localhost:4444')  # SOCKS5 прокси I2P
    app['connector'] = connector
    return app


async def clientside():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(50),
            proxy="http://localhost:4444"
    ) as session:
        async with session.get(DEST) as response:
            result = await response.read()
            print(result)
            print(KnapSack().deserialize(json.loads(result)))


def main():
    while True:
        match input('s/c >> '):
            case 's':
                web.run_app(serverside(), port=6626)
            case 'c':
                asyncio.run(clientside())
            case _:
                continue
        break


if __name__ == "__main__":
    main()
