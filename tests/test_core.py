import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

import deskally.config as config_module
from deskally.collectors import city, countdown, cpu_percent, human_bytes, local_ip, localized_date, memory_usage, public_ip, turkish_date
from deskally.config import DEFAULT_CONFIG, load_config, load_position, save_config, save_position
from deskally.i18n import STRINGS
from deskally.theme import resolve_color, set_accent


class CollectorTests(unittest.TestCase):
    def test_cpu_percent_uses_sample_delta(self):
        self.assertEqual(cpu_percent((100, 200), (125, 300)), 75)

    def test_memory_usage_from_proc_format(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meminfo"
            path.write_text("MemTotal: 1048576 kB\nMemAvailable: 524288 kB\n")
            self.assertEqual(memory_usage(path), "512MiB/1GiB • 50%")

    def test_turkish_date(self):
        self.assertEqual(turkish_date(datetime(2026, 10, 8)), "Perşembe 8 Ekim 2026")

    def test_countdown(self):
        now = datetime(2026, 10, 8, 10, 0, 0)
        self.assertEqual(countdown("2026-10-09T12:02:03", now, "tr"), "001 GÜN • 02:02:03")

    def test_english_date_and_countdown(self):
        now = datetime(2026, 10, 8, 10, 0, 0)
        self.assertEqual(localized_date("en", now), "Thursday 8 October 2026")
        self.assertEqual(
            countdown("2026-10-09T12:02:03", now, "en"),
            "001 DAYS • 02:02:03",
        )

    def test_translation_tables_have_matching_keys(self):
        self.assertEqual(set(STRINGS["tr"]), set(STRINGS["en"]))

    def test_human_bytes(self):
        self.assertEqual(human_bytes(1024 ** 3), "1GiB")

    def test_public_ip_uses_fallback_source(self):
        failed_curl = mock.Mock(returncode=1, stdout="")
        with mock.patch("deskally.collectors.subprocess.run", return_value=failed_curl), \
             mock.patch(
                 "deskally.collectors.fetch_text",
                 side_effect=[OSError("offline"), "198.51.100.20"],
             ):
            self.assertEqual(public_ip(), "198.51.100.20")

    def test_public_ip_accepts_cloudflare_trace(self):
        trace = "fl=1\nip=203.0.113.8\nloc=TR\n"
        failed_curl = mock.Mock(returncode=1, stdout="")
        with mock.patch("deskally.collectors.subprocess.run", return_value=failed_curl), \
             mock.patch("deskally.collectors.fetch_text", return_value=trace):
            self.assertEqual(public_ip(), "203.0.113.8")

    def test_public_ip_english_offline_message(self):
        failed_curl = mock.Mock(returncode=1, stdout="")
        with mock.patch("deskally.collectors.subprocess.run", return_value=failed_curl), \
             mock.patch("deskally.collectors.fetch_text", side_effect=OSError("offline")), \
             mock.patch("deskally.collectors.local_ip", return_value="—"):
            self.assertEqual(public_ip("en"), "No connection")

    def test_public_ip_prefers_working_ipv4_curl(self):
        completed = mock.Mock(returncode=0, stdout="ip=192.0.2.25\nloc=TR\n")
        with mock.patch("deskally.collectors.subprocess.run", return_value=completed), \
             mock.patch("deskally.collectors.fetch_text") as fetch:
            self.assertEqual(public_ip(), "192.0.2.25")
            fetch.assert_not_called()

    def test_local_ip_survives_blocked_socket(self):
        completed = mock.Mock(stdout="2: eth0 inet 192.168.1.42/24 brd 192.168.1.255\n")
        with mock.patch("deskally.collectors.socket.socket", side_effect=PermissionError), \
             mock.patch("deskally.collectors.subprocess.run", return_value=completed):
            self.assertEqual(local_ip(), "192.168.1.42")

    def test_city_prefers_ipv4_curl_result(self):
        completed = mock.Mock(returncode=0, stdout="Fethiye\n")
        with mock.patch("deskally.collectors.subprocess.run", return_value=completed):
            self.assertEqual(city(), "Fethiye")


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

    def test_unknown_language_falls_back_to_english(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text('{"language": "de"}')
            self.assertEqual(load_config(path)["language"], "en")

    def test_legacy_config_migrates_to_deskally_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            new_path = root / "deskally" / "config.json"
            legacy_path = root / "kundally-panel" / "config.json"
            legacy_path.parent.mkdir()
            legacy_path.write_text('{"title": "KundALLY", "language": "en"}')
            with mock.patch.object(config_module, "CONFIG_FILE", new_path), \
                 mock.patch.object(config_module, "LEGACY_CONFIG_FILE", legacy_path):
                loaded = load_config(new_path)
            self.assertEqual(loaded["title"], "DeskALLY")
            self.assertEqual(loaded["language"], "en")

    def test_position_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "position.json"
            save_position(12, 34, path)
            self.assertEqual(load_position(path), (12, 34))

    def test_theme_preset_preserves_other_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            save_config({**DEFAULT_CONFIG, "title": "Benim Panelim"}, path)
            self.assertEqual(set_accent("kırmızı", path), "#ff3b5c")
            loaded = load_config(path)
            self.assertEqual(loaded["title"], "Benim Panelim")
            self.assertEqual(loaded["accent_color"], "#ff3b5c")

    def test_custom_hex_color(self):
        self.assertEqual(resolve_color("#12ABef"), "#12abef")

    def test_english_color_alias(self):
        self.assertEqual(resolve_color("blue"), "#3b82f6")


if __name__ == "__main__":
    unittest.main()
