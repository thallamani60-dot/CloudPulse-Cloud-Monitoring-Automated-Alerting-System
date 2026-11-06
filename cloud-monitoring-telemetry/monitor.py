#!/usr/bin/env python3
"""Lightweight HTTP uptime monitor with JSONL history and webhook alerts."""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config.json"
DEFAULT_LOG = ROOT / "logs" / "uptime.jsonl"

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("timeout_seconds", 10)
    cfg.setdefault("latency_threshold_ms", 2000)
    cfg.setdefault("expected_status_codes", [200])
    cfg.setdefault("webhook_env_var", "ALERT_WEBHOOK_URL")
    cfg.setdefault("endpoints", [])
    return cfg

def check_endpoint(endpoint, cfg, simulate_failure=False):
    url = endpoint["url"]
    started = time.perf_counter()
    status = None
    error = None
    try:
        if simulate_failure:
            raise URLError("Simulated downtime for demonstration")
        req = Request(url, headers={"User-Agent": "cloud-telemetry-monitor/1.0"})
        with urlopen(req, timeout=cfg["timeout_seconds"]) as response:
            status = response.status
            response.read(128)
    except HTTPError as exc:
        status = exc.code
        error = f"HTTPError: {exc}"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    ok = status in cfg["expected_status_codes"] and error is None
    if latency_ms > cfg["latency_threshold_ms"]:
        ok = False
        error = (error + "; " if error else "") + "latency threshold exceeded"
    return {
        "timestamp": now_iso(),
        "name": endpoint.get("name", url),
        "url": url,
        "ok": ok,
        "status_code": status,
        "latency_ms": latency_ms,
        "error": error,
    }

def append_record(path, record):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def send_alert(record, webhook_url):
    message = {
        "text": (
            f"🚨 Uptime alert: {record['name']} is DOWN\n"
            f"URL: {record['url']}\n"
            f"HTTP status: {record['status_code']}\n"
            f"Latency: {record['latency_ms']} ms\n"
            f"Error: {record['error'] or 'Unknown'}\n"
            f"Time: {record['timestamp']}"
        )
    }
    data = json.dumps(message).encode("utf-8")
    req = Request(webhook_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=10) as response:
            print(f"[ALERT] Webhook delivered (HTTP {response.status})")
    except Exception as exc:
        print(f"[ALERT-FAILED] Could not deliver webhook: {exc}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="HTTP uptime and latency monitor")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--log", default=str(DEFAULT_LOG))
    parser.add_argument("--simulate-failure", action="store_true",
                        help="Force a failed check to demonstrate alerting")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if not cfg["endpoints"]:
        raise SystemExit("No endpoints configured in config.json")

    webhook = os.getenv(cfg["webhook_env_var"], "")
    failures = 0
    records = []
    for endpoint in cfg["endpoints"]:
        record = check_endpoint(endpoint, cfg, args.simulate_failure)
        append_record(Path(args.log), record)
        records.append(record)
        if record["ok"]:
            print(f"[UP] {record['name']} status={record['status_code']} latency={record['latency_ms']} ms")
        else:
            failures += 1
            print(f"[DOWN] {record['name']} status={record['status_code']} latency={record['latency_ms']} ms error={record['error']}")
            if webhook:
                send_alert(record, webhook)
            else:
                print(f"[ALERT] {record['name']} breached a monitoring threshold", file=sys.stderr)

    total = len(records)
    uptime = ((total - failures) / total * 100) if total else 0
    print(f"Summary: {total - failures}/{total} checks healthy | check-level availability: {uptime:.2f}%")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
