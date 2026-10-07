import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from kundally_panel.collectors import countdown, cpu_percent, human_bytes, local_ip, memory_usage, public_ip, turkish_date
from kundally_panel.config import DEFAULT_CONFIG, load_config, load_position, save_config, save_position


class CollectorTests(unittest.TestCase):
    def test_cpu_percent_uses_sample_delta(self):
        self.assertEqual(cpu_percent((100, 200), (125, 300)), 75)

    def test_memory_usage_from_proc_format(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meminfo"
            path.write_text("MemTotal: 1048576 kB\nMemAvailable: 524288 kB\n")
            self.assertEqual(memory_usage(path), "512MiB/1GiB")

    def test_turkish_date(self):
        self.assertEqual(turkish_date(datetime(2026, 10, 8)), "Perşembe 8 Ekim 2026")

    def test_countdown(self):
        now = datetime(2026, 10, 8, 10, 0, 0)
        self.assertEqual(countdown("2026-10-09T12:02:03", now), "001 GÜN • 02:02:03")

    def test_human_bytes(self):
        self.assertEqual(human_bytes(1024 ** 3), "1GiB")

    def test_public_ip_uses_fallback_source(self):
        failed_curl = mock.Mock(returncode=1, stdout="")
        with mock.patch("kundally_panel.collectors.subprocess.run", return_value=failed_curl), \
             mock.patch(
                 "kundally_panel.collectors.fetch_text",
                 side_effect=[OSError("offline"), "198.51.100.20"],
             ):
            self.assertEqual(public_ip(), "198.51.100.20")

    def test_public_ip_accepts_cloudflare_trace(self):
        trace = "fl=1\nip=203.0.113.8\nloc=TR\n"
        failed_curl = mock.Mock(returncode=1, stdout="")
        with mock.patch("kundally_panel.collectors.subprocess.run", return_value=failed_curl), \
             mock.patch("kundally_panel.collectors.fetch_text", return_value=trace):
            self.assertEqual(public_ip(), "203.0.113.8")

    def test_public_ip_prefers_working_ipv4_curl(self):
        completed = mock.Mock(returncode=0, stdout="ip=192.0.2.25\nloc=TR\n")
        with mock.patch("kundally_panel.collectors.subprocess.run", return_value=completed), \
             mock.patch("kundally_panel.collectors.fetch_text") as fetch:
            self.assertEqual(public_ip(), "192.0.2.25")
            fetch.assert_not_called()

    def test_local_ip_survives_blocked_socket(self):
        completed = mock.Mock(stdout="2: eth0 inet 192.168.1.42/24 brd 192.168.1.255\n")
        with mock.patch("kundally_panel.collectors.socket.socket", side_effect=PermissionError), \
             mock.patch("kundally_panel.collectors.subprocess.run", return_value=completed):
            self.assertEqual(local_ip(), "192.168.1.42")


class ConfigTests(unittest.TestCase):
    def test_round_trip_and_unknown_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            save_config({**DEFAULT_CONFIG, "title": "Test", "unknown": 42}, path)
            loaded = load_config(path)
            self.assertEqual(loaded["title"], "Test")
            self.assertNotIn("unknown", loaded)

    def test_bad_json_falls_back_to_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text("not json")
            self.assertEqual(load_config(path), DEFAULT_CONFIG)

    def test_position_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "position.json"
            save_position(12, 34, path)
            self.assertEqual(load_position(path), (12, 34))


if __name__ == "__main__":
    unittest.main()
