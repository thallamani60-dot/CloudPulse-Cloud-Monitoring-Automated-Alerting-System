# ☁️ CloudPulse – Cloud Monitoring & Automated Alerting System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green)
![Monitoring](https://img.shields.io/badge/Monitoring-HTTP%20Health%20Checks-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Project Overview

CloudPulse is a Python-based cloud monitoring and automated alerting system designed to monitor website and API availability.

It automatically performs HTTP health checks, measures response latency, tracks HTTP status codes, calculates uptime percentages, and generates alerts whenever a monitoring threshold is breached.

The project uses GitHub Actions for scheduled monitoring without requiring a paid cloud server.

## 🎯 Objectives

- Automate HTTP endpoint health monitoring.
- Measure response latency in milliseconds.
- Track HTTP status codes and service availability.
- Calculate uptime percentages.
- Generate automated alerts during service failures.
- Maintain historical monitoring logs.
- Automate monitoring through GitHub Actions.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Monitoring application |
| Git & GitHub | Version control |
| GitHub Actions | Scheduled automation |
| JSON / JSONL | Configuration and monitoring logs |
| Webhooks | Incident notifications |
| HTTP | Endpoint health checks |

## 🏗️ Project Architecture

```text
        Target Websites / APIs
                  |
                  v
          HTTP Health Checks
                  |
                  v
          Python Monitor Script
                  |
          +-------+-------+
          |               |
          v               v
    Latency Tracking   HTTP Status
          |               |
          +-------+-------+
                  |
                  v
          Threshold Evaluation
                  |
           +------+------+
           |             |
           v             v
        Healthy        Failure
           |             |
           v             v
       JSONL Logs    Alert Notification
                         |
                         v
                    Webhook Alert

             GitHub Actions
              (Every 5 min)
```

## 📂 Project Structure

```text
cloud-monitoring-telemetry/
│
├── .github/
│   └── workflows/
│       └── monitor.yml
│
├── logs/
│   └── uptime.jsonl
│
├── tests/
│   └── test_monitor.py
│
├── config.json
├── monitor.py
├── demo_server.py
├── requirements.txt
└── README.md
```

## ⚙️ Features

### 1. Automated Health Checks

- Sends HTTP requests to configured endpoints.
- Checks whether services are responding.
- Supports multiple monitoring targets.

### 2. Response Latency Monitoring

Measures response time in milliseconds.

Example:

```text
[UP] Example homepage status=200 latency=184.32 ms
```

### 3. HTTP Status Code Tracking

Monitors HTTP responses such as:

- 200 – OK
- 301 – Redirect
- 404 – Not Found
- 500 – Internal Server Error
- 503 – Service Unavailable

Only configured expected status codes are considered healthy.

### 4. Automated Alerting

CloudPulse generates alerts when:

- An endpoint becomes unavailable.
- An unexpected HTTP status is received.
- Response latency exceeds the configured threshold.

Notifications are available through console warnings and optional webhook integration.

### 5. Historical Uptime Logging

Monitoring results are stored in:

```text
logs/uptime.jsonl
```

Each record contains:

- Timestamp
- Endpoint name
- URL
- Availability status
- HTTP status code
- Response latency
- Error details

### 6. GitHub Actions Automation

The monitoring workflow runs automatically every five minutes.

Workflow file:

```text
.github/workflows/monitor.yml
```

It also supports manual execution through GitHub Actions.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Git
- GitHub account
- VS Code (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/cloudpulse-monitoring-alerting.git
```

### Step 2: Navigate to Project

```bash
cd cloudpulse-monitoring-alerting
```

### Step 3: Create Virtual Environment

Windows:

```powershell
py -3 -m venv .venv
.venv\Scripts\activate
```

### Step 4: Run Monitoring Script

```bash
python monitor.py
```

## 🧪 Testing and Downtime Simulation

CloudPulse includes a simulated monitoring environment.

### Start Local Demo Server

Terminal 1:

```bash
python demo_server.py
```

The local server provides:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/fail
```

- `/health` returns HTTP 200.
- `/fail` returns HTTP 503.

Configure the desired endpoint in `config.json`.

### Simulate Monitoring Failure

```bash
python monitor.py --simulate-failure
```

Expected output:

```text
[DOWN] Example homepage
status=None
latency=2.15 ms

[ALERT] Example homepage breached a monitoring threshold

Summary: 0/2 checks healthy
```

### Run Unit Tests

```bash
python -m unittest discover -s tests -v
```

## 🔔 Alert Configuration

Edit `config.json` to configure monitoring thresholds.

Example:

```json
{
  "timeout_seconds": 10,
  "latency_threshold_ms": 2000,
  "expected_status_codes": [200],
  "webhook_env_var": "ALERT_WEBHOOK_URL",
  "endpoints": [
    {
      "name": "My Website",
      "url": "https://example.com"
    }
  ]
}
```

### Webhook Setup

1. Create an incoming webhook with a supported notification provider.
2. Open your GitHub repository.
3. Navigate to Settings → Secrets and variables → Actions.
4. Select New repository secret.
5. Set the secret name to:

```text
ALERT_WEBHOOK_URL
```

6. Add your webhook URL as the secret value.

Never expose webhook URLs or tokens in public source code.

## 📊 Uptime Calculation

Uptime percentage is calculated using:

```text
Uptime (%) =
(Healthy Checks / Total Checks) × 100
```

Example:

| Total Checks | Successful | Failed | Uptime |
|---:|---:|---:|---:|
| 100 | 98 | 2 | 98% |
| 100 | 95 | 5 | 95% |
| 100 | 90 | 10 | 90% |

This is check-based availability, not continuous uptime measurement.

## ⚡ GitHub Actions Workflow

The monitoring workflow uses:

```yaml
on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:
```

Monitoring runs automatically every five minutes, subject to GitHub Actions scheduling delays.

To execute manually:

1. Open your GitHub repository.
2. Select Actions.
3. Open Cloud Telemetry Monitoring.
4. Click Run workflow.

## 📸 Project Screenshots

Add your actual execution screenshots here.

Recommended screenshots:

1. Healthy HTTP endpoint response.
2. Failed endpoint detection.
3. Console alert notification.
4. GitHub Actions workflow execution.
5. Historical uptime logs.
6. Local server health-check demonstration.

Example:

```markdown
![Successful Health Check](screenshots/healthy-check.png)

![Downtime Alert](screenshots/downtime-alert.png)

![GitHub Actions](screenshots/github-actions.png)
```

## 🎓 Learning Outcomes

Through this project, I gained practical experience in:

- Cloud monitoring fundamentals.
- Python automation and scripting.
- HTTP health checks and troubleshooting.
- Response latency measurement.
- Automated incident detection.
- Webhook integrations.
- GitHub Actions and scheduled workflows.
- Logging and uptime analysis.
- CI/CD automation concepts.

## 🔮 Future Enhancements

- Interactive monitoring dashboard.
- Historical uptime charts.
- Email and Telegram notifications.
- Multi-cloud monitoring integration.
- Prometheus and Grafana integration.
- Containerized monitoring using Docker.
- Alert deduplication and recovery notifications.

## ⚠️ Limitations

- GitHub Actions schedules may be delayed.
- Monitoring occurs at scheduled intervals rather than continuously.
- Uptime is estimated using individual health checks.
- Long-term production monitoring would benefit from dedicated time-series storage.

## 👨‍💻 Author

**Manikanta Thalla**

Computer Science Engineering – Internet of Things

Interests: Cloud Computing | Python | Linux | DevOps | Cloud Monitoring

GitHub: https://github.com/YOUR_USERNAME

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you find this project useful, consider giving it a star!
