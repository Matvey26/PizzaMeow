import asyncio
from typing import Iterable


async def aiter(object: Iterable):
    for item in object:
        yield item