import json

import aiohttp

from abstractions.knapclasses import KnapSack
from config import DEST
from misc import client_print as print


async def clientside():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(50),
            proxy="http://localhost:4444"
    ) as session:
        async with session.get(DEST) as response:
            result = await response.read()
            print(result)
            print(KnapSack().deserialize(json.loads(result)))
