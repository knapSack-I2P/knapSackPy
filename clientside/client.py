import json

import aiohttp

from abstractions.knapclasses import KnapSack
from shared.prettyIO import client_print as print


class Client:
    def __init__(self):
        ...

    async def run(self, address):
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(50),
                proxy="http://localhost:4444"
        ) as session:
            async with session.get(address) as response:
                result = await response.read()
                print(result)
                print(KnapSack().deserialize(json.loads(result)))
