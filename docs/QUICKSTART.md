# Quickstart Guide

Welcome to the SeeD Reboot initiative! This guide will help you get started with the project.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tpanarchist/S-d.git
   cd S-d
   ```

2. **Install dependencies:**
   Ensure you have Python 3.11 installed. Then, run:
   ```bash
   poetry install
   ```

## Running Cycles

To run the SeeD CLI for a specified number of cycles, use:
```bash
poetry run seed-run --cycles 30
```

## Plugin Selection

You can choose different Sense and Delta plugins using the `--sense` and `--delta` flags. For example:
```bash
poetry run seed-run --cycles 30 --sense jsonl --delta cosine
```

## Metrics

To enable the metrics server, use the `--metrics-port` flag. For example:
```bash
poetry run seed-run --cycles 30 --metrics-port 8000
```

You can then scrape the metrics by visiting `http://localhost:8000/metrics`.

## Exporting Logs

To export the event log, use:
```bash
python scripts/export_log.py --rows 1000 --out dumps/seed_log.jsonl.gz
```

This will export the last 1000 events to a gzipped JSONL file.
