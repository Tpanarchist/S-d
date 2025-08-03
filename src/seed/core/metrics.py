"""Prometheus-style metrics exposition for SeeD."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict

class Metrics:
    events_total: int = 0
    delta_mean: float = 0.0
    boredom_state_counts: Dict[str, int] = {"explore": 0, "steady": 0, "exploit": 0}

    @classmethod
    def increment(cls, flag: str, delta: float):
        cls.events_total += 1
        cls.delta_mean = ((cls.delta_mean * (cls.events_total - 1)) + delta) / cls.events_total
        if flag in cls.boredom_state_counts:
            cls.boredom_state_counts[flag] += 1

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; version=0.0.4')
            self.end_headers()
            response = (
                f"# HELP seed_events_total Total events processed\n"
                f"seed_events_total {Metrics.events_total}\n"
                f"# HELP seed_delta_mean Running mean Δ\n"
                f"seed_delta_mean {Metrics.delta_mean}\n"
                f"# HELP seed_boredom_state_total Total events per boredom flag\n"
                f"seed_boredom_state_total{{flag=\"explore\"}} {Metrics.boredom_state_counts['explore']}\n"
                f"seed_boredom_state_total{{flag=\"steady\"}} {Metrics.boredom_state_counts['steady']}\n"
                f"seed_boredom_state_total{{flag=\"exploit\"}} {Metrics.boredom_state_counts['exploit']}\n"
            )
            self.wfile.write(response.encode('utf-8'))

def start_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MetricsHandler)
    httpd.serve_forever()
