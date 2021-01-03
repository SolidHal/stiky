import asyncio

class Timer:
    def __init__(self, timeout, callback, args = None):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job(args))

    async def _job(self, args):
        await asyncio.sleep(self._timeout)
        if args != None:
            await self._callback(*args)
        else:
            await self._callback()

    def cancel(self):
        self._task.cancel()
