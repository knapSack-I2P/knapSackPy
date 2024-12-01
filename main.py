import asyncio

from aiohttp import web

from clientside.client import clientside
from serverside.server import serverside
from misc import server_print

async def cmd_handler():
    loop = asyncio.get_running_loop()
    while loop.is_running():
        print(await loop.run_in_executor(executor=None, func=input))


def main():
    loop = asyncio.new_event_loop()
    loop.create_task(web._run_app(serverside(), port=6626, print=server_print))
    loop.create_task(clientside())
    loop.create_task(cmd_handler())
    loop.run_forever()
    cmd, args = '', []


if __name__ == "__main__":
    main()
