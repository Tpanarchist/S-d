#!/usr/bin/env bash

# Run the SeeD CLI with metrics enabled
python -m seed.cli --cycles 50 --metrics-port 8000 &

# Allow some time for the server to start
sleep 5

# Fetch and display the first few lines of the metrics
curl -s http://localhost:8000/metrics | head

# Terminate the background process
kill %1
