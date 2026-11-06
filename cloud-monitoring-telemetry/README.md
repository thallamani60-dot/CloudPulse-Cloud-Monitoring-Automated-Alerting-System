# Cloud Monitoring — Telemetry & Automated Alerting

A small, free-to-run HTTP monitoring project built with Python and GitHub Actions. It records timestamp, HTTP status, latency (milliseconds), health state and errors as JSON Lines.

## Features

- Checks configured HTTP/HTTPS endpoints.
- Measures response latency with a monotonic high-resolution timer.
- Treats unexpected HTTP status, connection/timeout errors, and latency threshold breaches as incidents.
- Prints console alerts and optionally sends a JSON webhook notification.
- Stores historical checks in `logs/uptime.jsonl`.
- GitHub Actions runs every five minutes and commits updated history to the repository.

## Project structure

```text
.
├── .github/workflows/monitor.yml
├── config.json
├── monitor.py
├── demo_server.py
├── requirements.txt
├── logs/uptime.jsonl
└── tests/test_monitor.py
```

## Run locally (Windows PowerShell)

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python monitor.py
```

No third-party Python packages are required (the monitor uses the standard library).

## Configuration

Edit `config.json`:

- `timeout_seconds`: maximum time to wait for an endpoint.
- `latency_threshold_ms`: mark a check unhealthy if latency exceeds this value.
- `expected_status_codes`: HTTP status codes considered healthy.
- `endpoints`: list of named URLs to monitor.

Example:
```json
{
  "timeout_seconds": 10,
  "latency_threshold_ms": 1500,
  "expected_status_codes": [200, 204],
  "webhook_env_var": "ALERT_WEBHOOK_URL",
  "endpoints": [{"name": "My API", "url": "https://api.example.com/health"}]
}
```

## Simulate downtime and verify alerts

Terminal 1:
```powershell
python demo_server.py
```

Terminal 2: temporarily change an endpoint in `config.json` to `http://127.0.0.1:8000/fail`, then run:
```powershell
python monitor.py
```
Expected result: `[DOWN]`, HTTP `503`, a latency value in milliseconds, and a console alert. For a guaranteed simulated connection failure without changing the URL:
```powershell
python monitor.py --simulate-failure
```
Run the unit test:
```powershell
python -m unittest discover -s tests -v
```

## Webhook notifications

Create a webhook in a service that accepts JSON POST requests (for example, a Slack incoming webhook). In GitHub:
1. Open **Settings → Secrets and variables → Actions → New repository secret**.
2. Name it `ALERT_WEBHOOK_URL`.
3. Paste the webhook URL as the secret.
4. The workflow injects it as an environment variable. Do not hard-code webhook URLs or tokens in source control.

The payload uses a `text` field. Some webhook providers require a different JSON schema; adapt `send_alert()` for that provider.

## GitHub Actions setup

1. Push this project to a GitHub repository.
2. Open **Settings → Actions → General → Workflow permissions** and allow read/write permissions if repository policy requires it.
3. Ensure the workflow's `contents: write` permission is allowed.
4. Add `ALERT_WEBHOOK_URL` only if webhook alerts are desired.
5. Open **Actions → Cloud Telemetry Monitoring → Run workflow** for a manual test. Scheduled runs use `*/5 * * * *` (UTC).

GitHub may delay scheduled workflows during high load; this is not a hard real-time monitoring service. Public repositories generally receive scheduled workflows; private-repository minutes are subject to GitHub plan limits.

## Uptime calculation

Each JSONL row represents one endpoint check. Calculate availability over a time window as:

`uptime % = (healthy checks / total checks) × 100`

This is a check-based estimate, not a guarantee of continuous availability between checks. Example sample log contains three healthy checks and one failed check = 75% check-level availability.

## Evidence / screenshots for submission

Capture these screenshots after running the project:
1. Terminal showing a healthy check with status `200` and latency in `ms`.
2. Terminal showing a simulated `503` or `--simulate-failure` incident and alert.
3. GitHub Actions run showing a successful scheduled/manual workflow.
4. `logs/uptime.jsonl` showing multiple timestamped records.

Screenshots must come from your own execution; sample log rows are included as demonstration data and should not be represented as live production measurements.

## Limitations

- GitHub Actions is scheduled automation, not continuous 24/7 probing; schedules can be delayed.
- The workflow commits each run's JSONL log to the repository. For high-volume or production use, use external time-series storage and alert deduplication.
- The script exits with code 1 when any endpoint is unhealthy, making failures visible in workflow logs.
