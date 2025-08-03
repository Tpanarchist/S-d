import argparse
from rich.table import Table
from rich.console import Console
from seed.core.sense_bus import SENSE_REGISTRY
from seed.core.dyad_engine import load_delta
from seed.core.metrics import Metrics, start_server
from seed.plugins import autodiscover_plugins
from seed.core.boredom import BoredomThermostat
from seed.core.memory_log import MemoryLog
from seed.agents.self_test import audit_last

def main():
    parser = argparse.ArgumentParser(description="Run the SeeD CLI.")
    parser.add_argument("--cycles", type=int, default=100, help="Number of cycles to run")
    parser.add_argument("--sense", type=str, default="default", help="Sense plugin to use")
    parser.add_argument("--sense-path", type=str, help="Path for file/jsonl modes")
    parser.add_argument("--delta", type=str, default="ascii", help="Delta plugin to use")
    parser.add_argument("--metrics-port", type=int, default=8000, help="Port for metrics server (0 to disable)")
    parser.add_argument("--async", dest="async_mode", action="store_true", help="Run in async mode")
    parser.add_argument("--sync", dest="async_mode", action="store_false", help="Run in sync mode (default)")
    parser.set_defaults(async_mode=False)
    args = parser.parse_args()

    autodiscover_plugins()
    sense_fn = SENSE_REGISTRY.get(args.sense, SENSE_REGISTRY["default"])
    delta_fn = load_delta(args.delta)

    if args.metrics_port > 0:
        start_server(args.metrics_port)

    console = Console()
    memory_log = MemoryLog()
    boredom_thermostat = BoredomThermostat()

    if args.async_mode:
        from seed.core.runner_async import run
        asyncio.run(run(args.cycles, sense_fn, delta_fn, memory_log, boredom_thermostat))
    else:
        for cycle in range(1, args.cycles + 1):
            if args.sense_path and sense_fn.__code__.co_argcount > 0:
                sense_iter = sense_fn(path=args.sense_path)
            else:
                sense_iter = sense_fn()
            inp, contrast = next(sense_iter)
            d = delta_fn(inp, contrast)
            flag = boredom_thermostat.update(d)
            event = memory_log.append({"inp": inp, "contrast": contrast, "delta": d, "flag": flag})

            Metrics.increment(flag, d)

            if cycle % 5 == 0:
                table = Table(title="Recent Events")
                table.add_column("ID", justify="right", style="cyan", no_wrap=True)
                table.add_column("Input", style="magenta")
                table.add_column("Contrast", style="green")
                table.add_column("Delta", style="red")
                table.add_column("Flag", style="yellow")

                for event in memory_log.get_last_n_events(5):
                    table.add_row(*event.as_row())

                console.print(table)

            if cycle % 100 == 0:
                audit_last(100)

if __name__ == "__main__":
    main()
