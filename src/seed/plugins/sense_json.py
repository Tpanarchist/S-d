import json
import pathlib
import itertools
from seed.core.sense_bus import register

@register("jsonl")
def jsonl_reader(path: pathlib.Path = pathlib.Path("samples.jsonl")):
    lines = itertools.cycle(path.read_text().splitlines())
    while True:
        obj = json.loads(next(lines))
        yield obj["a"][0], obj["b"][0]
