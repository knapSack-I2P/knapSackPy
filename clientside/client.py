import json
from misc import client_print as print

import aiohttp

from abstractions.knapclasses import KnapSack
from config import DEST
import rich.repr

async def clientside():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(50),
            proxy="http://localhost:4444"
    ) as session:
        async with session.get(DEST) as response:
            result = await response.read()
            print(result)
            print(KnapSack().deserialize(json.loads(result)))
