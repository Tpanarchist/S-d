import pytest
from seed.core.runner_async import run
from seed.core.memory_log import MemoryLog
from seed.core.boredom import BoredomThermostat
from seed.core.sense_bus import SENSE_REGISTRY
from seed.core.dyad_engine import load_delta
from seed.core.metrics import Metrics

@pytest.mark.asyncio
async def test_async_runner():
    memory_log = MemoryLog()
    boredom_thermostat = BoredomThermostat()
    sense_fn = SENSE_REGISTRY["default"]
    delta_fn = load_delta("ascii")

    await run(50, sense_fn, delta_fn, memory_log, boredom_thermostat)

    assert Metrics.get_total_count() == 50
    assert Metrics.get_runtime() < 0.5
