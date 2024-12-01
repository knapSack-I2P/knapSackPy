import aiohttp
from aiohttp import web
from aiohttp_socks import ProxyConnector
import asyncio
import json
from config import DEST

from knapclasses import KnapSack

# DEST = "http://127.0.0.1:6626"


saved_videos: KnapSack = KnapSack()


def serverside():
    async def handle_default(request):
        return web.HTTPFound(location='/ping')

    async def handle_ping(request):
        print(request)
        print(saved_videos.serialize())
        return web.Response(body=json.dumps(saved_videos.serialize()),
                            content_type='')

    app = web.Application()
    app.router.add_get('/', handle_default)
    app.router.add_get('/ping', handle_ping)

    # SOCKS5 прокси I2P
    connector = ProxyConnector.from_url('socks5://localhost:4444')
    app['connector'] = connector
    return app


async def clientside():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(50),
                                     proxy="http://localhost:4444") as session:
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
