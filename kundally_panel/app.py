"""GTK 3 desktop panel application."""

from __future__ import annotations

import fcntl
import os
import re
import signal
import sys
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, GLib, Gtk, Pango

from . import __version__
from .collectors import (
    SystemCollector,
    city,
    countdown,
    default_interface,
    gpu_temperature,
    public_ip,
    turkish_date,
)
from .config import (
    LOCK_FILE,
    PID_FILE,
    POSITION_FILE,
    load_config,
    load_position,
    save_config,
    save_position,
)


BASE_CSS = """
window { background-color: transparent; }
#hud {
  background-color: rgba(5, 10, 18, 0.96);
  border: 1px solid ACCENT;
  border-radius: 16px;
  padding: 7px 9px;
  font-family: "DejaVu Sans";
}
#head { margin-bottom: 1px; }
#logo { color: ACCENT; font-size: 14px; font-weight: bold; }
#clock { color: white; font-size: 11px; font-weight: bold; }
#date { color: #cfefff; font-size: 8px; font-weight: bold; margin-bottom: 1px; }
#countdown {
  color: white;
  background-color: rgba(0, 229, 255, 0.10);
  border: 1px solid rgba(0, 229, 255, 0.25);
  border-radius: 5px;
  font-size: 9px;
  font-weight: bold;
  padding: 1px 4px;
  margin-bottom: 1px;
}
#title { color: ACCENT; font-size: 9px; font-weight: bold; margin: 1px 0; }
#line { background-color: ACCENT; min-height: 1px; margin: 1px 0; opacity: 0.5; }
#info {
  background-color: rgba(0, 220, 255, 0.06);
  border-radius: 6px;
  padding: 2px 5px;
  margin: 1px;
}
#key { color: #b5f6ff; font-size: 9px; font-weight: bold; }
#value { color: white; font-size: 9px; font-weight: bold; }
"""


class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent: Gtk.Window, config: dict) -> None:
        super().__init__(title="KundALLY Panel Ayarları", transient_for=parent, modal=True)
        self.add_buttons(
            "İptal", Gtk.ResponseType.CANCEL,
            "Kaydet", Gtk.ResponseType.OK,
        )
        self.set_default_size(390, -1)
        self.set_border_width(12)

        grid = Gtk.Grid(column_spacing=12, row_spacing=10)
        self.get_content_area().add(grid)

        grid.attach(Gtk.Label(label="Panel adı", xalign=0), 0, 0, 1, 1)
        self.title_entry = Gtk.Entry(text=config["title"])
        grid.attach(self.title_entry, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Geri sayım tarihi", xalign=0), 0, 1, 1, 1)
        self.target_entry = Gtk.Entry(text=config["countdown_target"])
        self.target_entry.set_placeholder_text("2027-08-15T00:00:00")
        grid.attach(self.target_entry, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Vurgu rengi", xalign=0), 0, 2, 1, 1)
        self.accent_entry = Gtk.Entry(text=config["accent_color"])
        self.accent_entry.set_placeholder_text("#00e5ff")
        grid.attach(self.accent_entry, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Panel genişliği", xalign=0), 0, 3, 1, 1)
        self.width_spin = Gtk.SpinButton.new_with_range(160, 420, 5)
        self.width_spin.set_value(config["panel_width"])
        grid.attach(self.width_spin, 1, 3, 1, 1)

        self.countdown_check = Gtk.CheckButton(label="Geri sayımı göster")
        self.countdown_check.set_active(config["show_countdown"])
        grid.attach(self.countdown_check, 0, 4, 2, 1)

        self.ip_check = Gtk.CheckButton(label="Genel IP adresini göster")
        self.ip_check.set_active(config["show_public_ip"])
        grid.attach(self.ip_check, 0, 5, 2, 1)

        self.location_check = Gtk.CheckButton(label="Şehir bilgisini göster")
        self.location_check.set_active(config["show_location"])
        grid.attach(self.location_check, 0, 6, 2, 1)

        self.top_check = Gtk.CheckButton(label="Diğer pencerelerin üstünde tut")
        self.top_check.set_active(config["always_on_top"])
        grid.attach(self.top_check, 0, 7, 2, 1)

        note = Gtk.Label(
            label="İpucu: Paneli sol tuşla tutup sürükle. Menüyü sağ tıkla aç.",
            xalign=0,
        )
        note.set_line_wrap(True)
        grid.attach(note, 0, 8, 2, 1)
        self.show_all()

    def values(self) -> dict:
        return {
            "title": self.title_entry.get_text().strip() or "KundALLY",
            "countdown_target": self.target_entry.get_text().strip(),
            "show_countdown": self.countdown_check.get_active(),
            "show_public_ip": self.ip_check.get_active(),
            "show_location": self.location_check.get_active(),
            "always_on_top": self.top_check.get_active(),
            "accent_color": self.accent_entry.get_text().strip(),
            "panel_width": self.width_spin.get_value_as_int(),
        }


class KundallyPanel(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="KundALLY Panel")
        self.config = load_config()
        self.collector = SystemCollector()
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="kundally")
        self.running: set[str] = set()
        self.labels: dict[str, Gtk.Label] = {}
        self.rows: dict[str, Gtk.Widget] = {}
        self.position_timer: int | None = None
        self.position_ready = False
        self.alive = True

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(self.config["always_on_top"])
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_app_paintable(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.apply_css()

        self.drag_area = Gtk.EventBox()
        self.drag_area.set_visible_window(False)
        self.drag_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drag_area.connect("button-press-event", self.on_pointer_press)
        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "move")
        if cursor:
            self.drag_area.connect("realize", lambda widget: widget.get_window().set_cursor(cursor))

        self.hud = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hud.set_name("hud")
        self.hud.set_size_request(self.config["panel_width"], -1)
        self.drag_area.add(self.hud)
        self.add(self.drag_area)
        self.build_content()
        self.context_menu = self.build_menu()

        self.connect("configure-event", self.on_configure)
        self.connect("destroy", self.on_destroy)
        self.connect("delete-event", lambda *_: Gtk.main_quit())

        GLib.timeout_add_seconds(1, self.update_time)
        self.update_time()
        self.jobs = {
            "wan": (public_ip, 60),
            "iface": (default_interface, 10),
            "city": (city, 300),
            "cpu": (self.collector.cpu, 5),
            "gput": (gpu_temperature, 5),
            "ram": (self.collector.ram, 10),
        }
        for name, (_function, interval) in self.jobs.items():
            self.refresh(name)
            GLib.timeout_add_seconds(interval, self.refresh, name)

    def apply_css(self) -> None:
        accent = self.config.get("accent_color", "#00e5ff")
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
            accent = "#00e5ff"
            self.config["accent_color"] = accent
        provider = Gtk.CssProvider()
        provider.load_from_data(BASE_CSS.replace("ACCENT", accent).encode())
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    @staticmethod
    def make_label(text: str, name: str, align: float) -> Gtk.Label:
        widget = Gtk.Label(label=text)
        widget.set_name(name)
        widget.set_xalign(align)
        return widget

    def build_content(self) -> None:
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.set_name("head")
        self.labels["logo"] = self.make_label(
            f"◉ {self.config['title']}", "logo", 0.0
        )
        self.labels["clock"] = self.make_label("--:--", "clock", 1.0)
        header.pack_start(self.labels["logo"], False, False, 0)
        header.pack_end(self.labels["clock"], False, False, 0)
        self.hud.pack_start(header, False, False, 0)

        self.labels["date"] = self.make_label("…", "date", 0.0)
        self.hud.pack_start(self.labels["date"], False, False, 0)
        self.labels["countdown"] = self.make_label("…", "countdown", 0.5)
        self.labels["countdown"].set_no_show_all(True)
        self.hud.pack_start(self.labels["countdown"], False, False, 0)

        self.add_line()
        self.hud.pack_start(self.make_label("NETWORK", "title", 0.0), False, False, 0)
        self.add_row("WAN", "wan")
        self.add_row("IF", "iface")
        self.add_row("LOC", "city")
        self.add_line()
        self.hud.pack_start(self.make_label("SYSTEM", "title", 0.0), False, False, 0)
        self.add_row("CPU", "cpu")
        self.add_row("GPU", "gput")
        self.add_row("RAM", "ram")
        self.update_visibility()

    def add_line(self) -> None:
        line = Gtk.Box()
        line.set_name("line")
        self.hud.pack_start(line, False, False, 0)

    def add_row(self, key: str, name: str) -> None:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.set_name("info")
        value = self.make_label("…", "value", 1.0)
        value.set_ellipsize(Pango.EllipsizeMode.END)
        value.set_max_width_chars(24)
        row.pack_start(self.make_label(key, "key", 0.0), False, False, 0)
        row.pack_end(value, True, True, 0)
        self.hud.pack_start(row, False, False, 0)
        self.labels[name] = value
        self.rows[name] = row
        if name in ("wan", "city"):
            row.set_no_show_all(True)

    def build_menu(self) -> Gtk.Menu:
        menu = Gtk.Menu()
        for title, callback in (
            ("Şimdi yenile", self.refresh_all),
            ("Ayarlar", self.open_settings),
            ("Konumu sıfırla", self.reset_position),
            ("Hakkında", self.show_about),
            ("Kapat", lambda *_: Gtk.main_quit()),
        ):
            item = Gtk.MenuItem(label=title)
            item.connect("activate", callback)
            menu.append(item)
        menu.show_all()
        return menu

    def on_pointer_press(self, _widget: Gtk.Widget, event: Gdk.EventButton) -> bool:
        if event.button == 1:
            self.begin_move_drag(1, int(event.x_root), int(event.y_root), event.time)
            return True
        if event.button == 3:
            self.context_menu.popup_at_pointer(event)
            return True
        return False

    def update_time(self) -> bool:
        now = datetime.now()
        self.labels["clock"].set_text(now.strftime("%H:%M"))
        self.labels["date"].set_text(turkish_date(now))
        self.labels["countdown"].set_text(countdown(self.config["countdown_target"], now))
        return self.alive

    def refresh(self, name: str) -> bool:
        if not self.alive or name in self.running:
            return self.alive
        if name == "wan" and not self.config["show_public_ip"]:
            return True
        if name == "city" and not self.config["show_location"]:
            return True
        function = self.jobs[name][0]
        self.running.add(name)
        future = self.executor.submit(function)
        future.add_done_callback(
            lambda completed, field=name: GLib.idle_add(self.apply_result, field, completed)
        )
        return True

    def apply_result(self, name: str, future: Future) -> bool:
        self.running.discard(name)
        if not self.alive:
            return False
        try:
            value = str(future.result()).strip() or "—"
        except Exception:
            value = "—"
        self.labels[name].set_text(value)
        self.labels[name].set_tooltip_text(f"Son yenileme: {datetime.now():%H:%M:%S}")
        return False

    def refresh_all(self, *_args) -> None:
        for name in self.jobs:
            self.refresh(name)

    def open_settings(self, *_args) -> None:
        dialog = SettingsDialog(self, self.config)
        if dialog.run() == Gtk.ResponseType.OK:
            self.config.update(dialog.values())
            save_config(self.config)
            self.labels["logo"].set_text(f"◉ {self.config['title']}")
            self.hud.set_size_request(self.config["panel_width"], -1)
            self.set_keep_above(self.config["always_on_top"])
            self.apply_css()
            self.update_visibility()
            self.update_time()
            self.refresh_all()
        dialog.destroy()

    def update_visibility(self) -> None:
        self.labels["countdown"].set_visible(self.config["show_countdown"])
        self.rows["wan"].set_visible(self.config["show_public_ip"])
        self.rows["city"].set_visible(self.config["show_location"])

    def show_about(self, *_args) -> None:
        dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        dialog.set_program_name("KundALLY Panel")
        dialog.set_version(__version__)
        dialog.set_comments("Linux masaüstü için sürüklenebilir sistem ve ağ paneli.")
        dialog.set_website("https://github.com/")
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.run()
        dialog.destroy()

    def place_initially(self) -> bool:
        saved = load_position()
        if saved:
            self.move(*saved)
        else:
            screen = self.get_screen()
            monitor = screen.get_primary_monitor()
            if monitor < 0:
                monitor = 0
            area = screen.get_monitor_workarea(monitor)
            width, height = self.get_size()
            self.move(area.x + area.width - width - 12,
                      area.y + area.height - height - 12)
        self.position_ready = True
        return False

    def reset_position(self, *_args) -> None:
        try:
            POSITION_FILE.unlink()
        except FileNotFoundError:
            pass
        self.position_ready = False
        self.place_initially()

    def on_configure(self, *_args) -> bool:
        if self.position_ready and self.position_timer is None:
            self.position_timer = GLib.timeout_add(250, self.persist_position)
        return False

    def persist_position(self) -> bool:
        self.position_timer = None
        save_position(*self.get_position())
        return False

    def on_destroy(self, *_args) -> None:
        self.alive = False
        self.executor.shutdown(wait=False, cancel_futures=True)
        try:
            if PID_FILE.read_text().strip() == str(os.getpid()):
                PID_FILE.unlink()
        except OSError:
            pass
        Gtk.main_quit()


def main() -> int:
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    lock_handle = LOCK_FILE.open("w")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("KundALLY Panel zaten çalışıyor.", file=sys.stderr)
        return 0

    PID_FILE.write_text(f"{os.getpid()}\n", encoding="utf-8")
    signal.signal(signal.SIGTERM, lambda *_: GLib.idle_add(Gtk.main_quit))
    panel = KundallyPanel()
    panel.show_all()
    GLib.idle_add(panel.place_initially)
    Gtk.main()
    lock_handle.close()
    return 0
