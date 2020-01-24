import socket
import asyncio
import aiodns


class AsyncTraceroute:
    def __init__(self, dest, port=33434, max_hops=30, timeout=1, packet_size=60):
        assert isinstance(dest, str), "dest should be an instance of str"
        assert isinstance(port, int), "port should be an instance of int"
        assert isinstance(max_hops, int), "max_hops should be an instance of int"
        assert isinstance(timeout, int), "timeout should be an instance of int"
        try:
            socket.inet_aton(dest)
            self.dest_addr = dest
        except socket.error:
            self.dest_addr = socket.gethostbyname(dest)
        self.port = port
        self.max_hops = max_hops
        self.timeout = timeout
        self.packet_size = packet_size
        self.i = 0
        self._ttl = 0
        self._loop = asyncio.get_event_loop()
        self._resolver = aiodns.DNSResolver(loop=self._loop)
        self._queue = asyncio.Queue()
        self._rx = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self._tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._loop.add_reader(
            self._rx, lambda: self._queue.put_nowait(self._rx.recvfrom(512))
        )

    def _stop(self):
        self._loop.remove_reader(self._rx)

    async def run(self):
        return [res async for res in self]

    def __iter__(self):
        raise RuntimeError("You need to use the syntax 'async for'")

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._ttl == self.max_hops:
            self._stop()
            raise StopAsyncIteration

        try:
            self._ttl += 1
            self.i += 1
            self._tx.setsockopt(socket.SOL_IP, socket.IP_TTL, self._ttl)
            self._tx.sendto(b"X" * self.packet_size, (self.dest_addr, self.port))
            next_addr = name = None
            try:
                _, addr = await asyncio.wait_for(self._queue.get(), self.timeout)
                next_addr = addr[0]
                if next_addr == self.dest_addr:
                    self._ttl = self.max_hops
                res = await self._resolver.gethostbyaddr(next_addr)
                name = res.name
            except asyncio.TimeoutError:
                pass
            except aiodns.error.DNSError:
                pass

            return self.i, next_addr, name
        except:
            self._stop()
            raise
