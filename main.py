import asyncio
from aiohttp import web

from abstractions.knapclasses import KnapSack

DEST = "http://hr4zbelmgfioktfgrah6a6a2o7gsfgsq7wbxscll3kf2okpqgvga.b32.i2p/"
# DEST = "http://127.0.0.1:6626"


saved_videos: KnapSack = KnapSack()

from clientside.client import clientside
from misc import server_print
from serverside.server import serverside


def main():
    loop = asyncio.new_event_loop()
    loop.create_task(web._run_app(serverside(), port=6626, print=server_print))
    loop.create_task(clientside())
    loop.run_forever()


if __name__ == "__main__":
    main()
