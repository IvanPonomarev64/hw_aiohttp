import aiohttp
import asyncio
from reque import logging, post_adv, get_adv, del_adv


HOST = "http://0.0.0.0:8080"


async def main():
    async with aiohttp.ClientSession() as session:
        # Create owner
        async with session.post(f"{HOST}/owners/", json=logging) as response:
            resp = await response.json()
            print(resp)

        # async with session.post(f"{HOST}/login/", json=logging) as response:
        #     resp = await response.text()
        #     print(resp)

        # async with session.post(f"{HOST}/post-adv/", json=post_adv) as response:
        #     resp = await response.json()
        #     print(resp)
        #
        # async with session.get(f"{HOST}/get-adv/", json=get_adv) as response:
        #     resp = await response.json()
        #     print(resp)
        #
        # async with session.delete(f"{HOST}/delete-adv/", json=del_adv) as response:
        #     resp = await response.text()
        #     print(resp)


if __name__ == "__main__":
    asyncio.run(main())
