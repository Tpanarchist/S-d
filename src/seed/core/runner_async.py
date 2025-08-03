import asyncio
from src.seed.util.pg_helpers import acquire_connection

async def run(cycles: int, sense_fn, delta_fn, log, thermo):
    i = 0
    async for a, b in sense_fn():  # sense_fn yields async iterable
        d = delta_fn(a, b)
        flag = thermo.update(d)
        async with acquire_connection() as conn:
            await log.append_async({...})
        Metrics.increment(flag, d)
        i += 1
        if cycles and i >= cycles:
            break
