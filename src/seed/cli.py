import argparse
from rich.table import Table
from rich.console import Console
from seed.core.sense_bus import read
from seed.core.dyad_engine import delta
from seed.core.boredom import BoredomThermostat
from seed.core.memory_log import MemoryLog
from seed.agents.self_test import audit_last

def main():
    parser = argparse.ArgumentParser(description="Run the SeeD CLI.")
    parser.add_argument("--cycles", type=int, default=100, help="Number of cycles to run")
    args = parser.parse_args()

    console = Console()
    memory_log = MemoryLog()
    boredom_thermostat = BoredomThermostat()

    for cycle in range(1, args.cycles + 1):
        inp, contrast = read()
        d = delta(inp, contrast)
        flag = boredom_thermostat.update(d)
        memory_log.append({"inp": inp, "contrast": contrast, "delta": d, "flag": flag})

        if cycle % 5 == 0:
            table = Table(title="Recent Events")
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Input", style="magenta")
            table.add_column("Contrast", style="green")
            table.add_column("Delta", style="red")
            table.add_column("Flag", style="yellow")

            for event in memory_log.get_last_n_events(5):
                table.add_row(str(event[0]), event[1], event[2], f"{event[3]:.4f}", str(event[4]))

            console.print(table)

        if cycle % 100 == 0:
            audit_last(100)

if __name__ == "__main__":
    main()
