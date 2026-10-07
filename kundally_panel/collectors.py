"""Small, dependency-free Linux system information collectors."""

from __future__ import annotations

import re
import socket
import subprocess
import urllib.request
from datetime import datetime
from ipaddress import ip_address
from pathlib import Path


DAYS_TR = (
    "Pazartesi", "Salı", "Çarşamba", "Perşembe",
    "Cuma", "Cumartesi", "Pazar",
)
MONTHS_TR = (
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
)


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    number = float(value)
    for unit in units:
        if abs(number) < 1024.0 or unit == units[-1]:
            return f"{number:.0f}{unit}" if unit != "B" else f"{int(number)}B"
        number /= 1024.0
    return f"{number:.0f}TiB"


def read_cpu_sample(path: Path = Path("/proc/stat")) -> tuple[int, int]:
    values = path.read_text(encoding="utf-8").splitlines()[0].split()[1:]
    ticks = [int(value) for value in values]
    idle = ticks[3] + (ticks[4] if len(ticks) > 4 else 0)
    return idle, sum(ticks)


def cpu_percent(previous: tuple[int, int], current: tuple[int, int]) -> int:
    idle_delta = current[0] - previous[0]
    total_delta = current[1] - previous[1]
    if total_delta <= 0:
        return 0
    return max(0, min(100, round(100 * (1 - idle_delta / total_delta))))


def memory_usage(path: Path = Path("/proc/meminfo")) -> str:
    values: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, raw = line.split(":", 1)
        match = re.search(r"\d+", raw)
        if match:
            values[key] = int(match.group()) * 1024
    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", values.get("MemFree", 0))
    return f"{human_bytes(max(0, total - available))}/{human_bytes(total)}"


def default_interface(path: Path = Path("/proc/net/route")) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines()[1:]:
            fields = line.split()
            if len(fields) > 3 and fields[1] == "00000000" and int(fields[3], 16) & 2:
                return fields[0]
    except (OSError, ValueError):
        pass
    return "—"


def _read_temperature(patterns: tuple[str, ...]) -> str:
    candidates: list[tuple[int, str]] = []
    for hwmon in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            name = (hwmon / "name").read_text().strip().lower()
        except OSError:
            continue
        if not any(pattern in name for pattern in patterns):
            continue
        for sensor in hwmon.glob("temp*_input"):
            try:
                millidegrees = int(sensor.read_text().strip())
                if 0 < millidegrees < 150_000:
                    candidates.append((millidegrees, name))
            except (OSError, ValueError):
                continue
    if candidates:
        value, _name = max(candidates)
        return f"{value / 1000:.1f}°C"
    return "—"


def cpu_temperature() -> str:
    return _read_temperature(("coretemp", "k10temp", "zenpower", "cpu"))


def gpu_temperature() -> str:
    value = _read_temperature(("amdgpu", "nvidia", "nouveau", "radeon"))
    if value != "—":
        return value
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=2, check=False,
        ).stdout.splitlines()
        return f"{result[0].strip()}°C" if result else "—"
    except (OSError, subprocess.SubprocessError):
        return "—"


def fetch_text(url: str, timeout: float = 5.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "KundALLY-Panel/0.2"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(256).decode("utf-8", "replace").strip()


def public_ip() -> str:
    sources = (
        ("https://www.cloudflare.com/cdn-cgi/trace", True),
        ("https://api.ipify.org", False),
        ("https://ident.me", False),
        ("https://ifconfig.me/ip", False),
    )
    for url, is_trace in sources:
        try:
            response = fetch_text(url)
            candidate = response
            if is_trace:
                candidate = next(
                    (line.removeprefix("ip=").strip() for line in response.splitlines()
                     if line.startswith("ip=")),
                    "",
                )
            ip_address(candidate)
            return candidate
        except Exception:
            continue
    return "—"


def city() -> str:
    for url in ("https://ipinfo.io/city", "https://ipapi.co/city/"):
        try:
            value = fetch_text(url)
            if value and "error" not in value.lower():
                return value.splitlines()[0]
        except Exception:
            continue
    return "—"


def local_hostname() -> str:
    return socket.gethostname() or "—"


def turkish_date(moment: datetime | None = None) -> str:
    moment = moment or datetime.now()
    return f"{DAYS_TR[moment.weekday()]} {moment.day} {MONTHS_TR[moment.month]} {moment.year}"


def countdown(target_text: str, moment: datetime | None = None) -> str:
    moment = moment or datetime.now()
    try:
        target = datetime.fromisoformat(target_text)
    except ValueError:
        return "Tarih ayarlanmadı"
    seconds = max(0, int((target - moment).total_seconds()))
    days, seconds = divmod(seconds, 86_400)
    hours, seconds = divmod(seconds, 3_600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days:03d} GÜN • {hours:02d}:{minutes:02d}:{seconds:02d}"


class SystemCollector:
    """Keeps the previous CPU sample while exposing display-ready values."""

    def __init__(self) -> None:
        try:
            self.previous_cpu = read_cpu_sample()
        except (OSError, ValueError, IndexError):
            self.previous_cpu = (0, 0)

    def cpu(self) -> str:
        try:
            current = read_cpu_sample()
            value = cpu_percent(self.previous_cpu, current)
            self.previous_cpu = current
            return f"{value}% {cpu_temperature()}"
        except (OSError, ValueError, IndexError):
            return "—"

    @staticmethod
    def ram() -> str:
        try:
            return memory_usage()
        except (OSError, ValueError):
            return "—"
