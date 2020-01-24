# Simple asynchronous traceroute

Dead simple module which provides asynchronous traceroute with asynchronous dns resolution.

Needs root privileges to be executed (for raw socket)
## Example

```python
import asyncio
from aiotraceroute import AsyncTraceroute

async def main(dest):
	# print hop by hop
	async for n, addr, host in AsyncTraceroute(dest):
		print(n, addr, host)

	# Or run it without iterating
	tr = AsyncTraceroute(dest)
	result = await tr.run()
	print(result)

asyncio.get_event_loop().run_until_complete(main("google.com"))
```
## API
The `AsyncTraceroute` class takes the following arguments:
  * `dest`: Traceroute destination, can either be a hostname or an IP address.
  * `port`: Destination port (optionnal, default: 33333)
  * `max_hops`: Maximum number of hops before reaching final destination (optionnal, default: 30)
  * `timeout`: Timeout between each hop (optionnal: default: 1s)
  * `packet_size`: Pakcte size in bytes to send each time (optionnal: default: 60)

The `run()` method runs the traceroute and returns a list of tuples containing hop_number, address or None, hostname or None
## Python versions
Python >= 3.6 are supported
