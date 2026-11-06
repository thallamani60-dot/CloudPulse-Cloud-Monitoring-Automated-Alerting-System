import unittest
from monitor import check_endpoint

class MonitorTests(unittest.TestCase):
    def test_simulated_failure_is_down(self):
        cfg = {"timeout_seconds": 1, "latency_threshold_ms": 2000, "expected_status_codes": [200]}
        result = check_endpoint({"name": "demo", "url": "http://127.0.0.1:8000/health"}, cfg, True)
        self.assertFalse(result["ok"])
        self.assertIsNotNone(result["error"])

if __name__ == "__main__":
    unittest.main()
