import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from kundally_panel.collectors import countdown, cpu_percent, human_bytes, memory_usage, public_ip, turkish_date
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
        with mock.patch(
            "kundally_panel.collectors.fetch_text",
            side_effect=[OSError("offline"), "198.51.100.20"],
        ):
            self.assertEqual(public_ip(), "198.51.100.20")


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
