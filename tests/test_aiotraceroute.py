import unittest
import asyncio
import aiodns
import socket
from context import aiotraceroute


def async_test(f):
    def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))

    return wrapper


class BasicTestSuite(unittest.TestCase):
    @async_test
    async def test_if_dest_correct(self):
        host = "www.google.com"
        dest_addr = socket.gethostbyname(host)
        found_addr = None
        async for n, addr, host in aiotraceroute.aiotraceroute(host):
            found_addr = addr
        self.assertEqual(found_addr, dest_addr)

    @async_test
    async def test_if_max_hops(self):
        results = []
        max_hops = 1
        host = "www.google.com"
        async for infos in aiotraceroute.aiotraceroute(host, max_hops=max_hops):
            results.append(aiotraceroute)
        self.assertEqual(max_hops, len(results))

    @async_test
    async def test_run(self):
        results = []
        max_hops = 2
        host = "www.google.com"
        tr = await aiotraceroute.aiotraceroute(host, max_hops=max_hops).run()
        self.assertEqual(len(tr), max_hops)


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        pass
