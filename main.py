import asyncio

from aiohttp import web

from clientside.client import clientside
from serverside.server import serverside
from misc import server_print
from test import partition
from config import FILE_DIRECTORY


async def cmd_handler():
    loop = asyncio.get_running_loop()
    while loop.is_running():
        cmd = (await loop.run_in_executor(executor=None, func=input)).split()
        match cmd:
            case ['seed']:
                ...
            case 'seed', *args:
                print(partition(*args))


def prep():
    FILE_DIRECTORY.mkdir(exist_ok=True)


def main():
    prep()
    loop = asyncio.new_event_loop()
    loop.create_task(web._run_app(serverside(), port=6626, print=server_print))
    loop.create_task(clientside())
    loop.create_task(cmd_handler())
    loop.run_forever()


if __name__ == "__main__":
    main()
