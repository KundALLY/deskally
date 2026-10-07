# DeskALLY

[Türkçe](README.md) · [English](README.en.md)

![DeskALLY preview](docs/preview.svg)

DeskALLY is an open source GTK 3 application that displays essential system and network information in a compact Linux desktop window. It keeps CPU, GPU, RAM, IP addresses, city, date, time, and a personal countdown visible at a glance.

The panel has no title bar. You can drag it directly with the mouse, it remembers its last position, and it resizes when optional rows are hidden. The interface is available in Turkish and English.

## Features

- CPU usage and temperature, GPU temperature, RAM usage and percentage
- Active network interface, local IP, public WAN IP, and approximate city
- Personal countdown configured with calendar and time controls
- Turkish and English interface, date, and countdown text
- Custom panel title, accent color, and width
- Independent visibility controls for WAN IP, local IP, city, and countdown
- Manual city override when automatic detection is unavailable
- Direct mouse dragging, saved position, and a right-click menu
- Automatic start at login
- Management through one `deskally` command
- Per-user installation with no administrator access required

## Supported systems

The application targets Debian, Ubuntu, Linux Mint, and similar Linux distributions with GTK 3. It works on X11 desktops. Window placement and always-on-top behavior may depend on the desktop compositor when running under Wayland.

## Requirements

Install the required packages on Debian-based systems:

```bash
sudo apt install python3 python3-gi gir1.2-gtk-3.0
```

For broader temperature sensor support, optionally install:

```bash
sudo apt install lm-sensors
```

## Installation

Download and extract the project from **Code → Download ZIP** on GitHub, or clone the repository. When the repository is published, `KULLANICI_ADI` in this example will be replaced with the actual GitHub username:

```bash
git clone https://github.com/KULLANICI_ADI/deskally.git
cd deskally
./install.sh
```

The installer copies the application under `~/.local`, creates application menu and autostart entries, and starts the panel. If `~/.local/bin` is not in PATH, sign out and back in.

To install without starting the panel immediately:

```bash
./install.sh --no-start
```

## First use

1. Hold the left mouse button anywhere on the panel and drag it.
2. Click the **⚙** button at the top right to open settings.
3. Choose **Türkçe** or **English** from the **Language** list.
4. Configure the title, color, width, countdown, and visible rows.
5. Click **Save**. Changes take effect immediately.
6. Right-click the panel to refresh, reset its position, or quit.

## Command guide

| Command | Purpose |
| --- | --- |
| `deskally start` | Starts the panel and avoids opening a duplicate instance. |
| `deskally stop` | Stops the running panel. |
| `deskally restart` | Stops and starts the panel with the latest settings. |
| `deskally status` | Shows whether the panel is running and prints its PID. |
| `deskally logs` | Prints the last 100 log lines. |
| `deskally color COLOR` | Changes the accent color and restarts the panel. |
| `deskally version` | Prints the installed version. |
| `deskally help` | Shows the short command reference. |

Turkish command aliases are also available: `baslat`, `durdur`, `yenile`, `durum`, `gunluk`, `renk`, `surum`, and `yardim`.

### Color command

Preset colors accept English or Turkish names:

```bash
deskally color cyan
deskally color blue
deskally color red
deskally color green
deskally color purple
deskally color gold
```

Their Turkish equivalents are `turkuaz`, `mavi`, `kirmizi`, `yesil`, `mor`, and `altin`. Use a six-digit HEX value for a custom color:

```bash
deskally color '#ff8800'
```

The color command preserves the title, language, countdown, and visibility settings.

## Displayed information

| Label | Meaning |
| --- | --- |
| `WAN` | The public IP address visible on the internet |
| `IF` | Default network interface, such as `enp10s0` or `wlan0` |
| `IP` | IPv4 address on the local network |
| `LOC` | Approximate city from the public IP, or the manual city value |
| `CPU` | Processor usage and temperature when available |
| `GPU` | Graphics processor temperature when available |
| `RAM` | Used/total memory and usage percentage |

An em dash (`—`) means the value could not be read from the hardware or operating system.

## Settings

- **Panel name:** Personal title displayed at the top.
- **Language:** Turkish or English. Saving updates the panel, menu, and next settings window.
- **Countdown date and time:** Target date and time for the countdown.
- **Panel color:** Changes the accent through a visual color picker.
- **Panel width:** Adjustable from 160 to 420 pixels.
- **City:** Automatic when empty; a manual value replaces the `LOC` result.
- **Visibility options:** Countdown, WAN IP, local IP, and city can be hidden independently.
- **Keep above other windows:** Requests always-on-top behavior from the desktop environment.

## File locations

| Location | Contents |
| --- | --- |
| `~/.local/share/deskally/` | Installed application files |
| `~/.local/bin/deskally` | User command |
| `~/.local/share/applications/deskally.desktop` | Application menu entry |
| `~/.config/autostart/deskally.desktop` | Login autostart entry |
| `~/.config/deskally/config.json` | User settings |
| `~/.local/state/deskally/` | PID, position, and log files |

## Privacy and network use

Local IP and system values are read locally. When WAN IP is enabled, the panel may send a short request to Cloudflare Trace, ipify, ident.me, or ifconfig.me. When city detection is enabled, it may use ipinfo.io, ipapi.co, ipwho.is, or ip-api.com.

These services naturally see the public IP making the request. WAN IP and city can be disabled independently in settings. Entering a manual city prevents the city lookup.

## Troubleshooting

If the panel does not open, check its status and logs first:

```bash
deskally status
deskally logs
deskally restart
```

If the shell reports `deskally: command not found`, make sure `~/.local/bin` is in PATH or use the full path:

```bash
~/.local/bin/deskally restart
```

If the city is empty, check the internet connection or enter it in **Settings → City**. If a temperature shows `—`, install `lm-sensors` and verify that the hardware exposes a supported sensor. If an enabled row is missing, restart the panel. If the panel is outside the visible desktop, use **Reset position** in the right-click menu.

## Updating

After downloading a newer source version, run the installer again inside the project directory:

```bash
./install.sh
```

Personal settings and the saved panel position are preserved.

## Uninstalling

From the project directory:

```bash
./uninstall.sh
```

The uninstaller removes the application, command, menu entry, and autostart entry. It preserves personal settings for a future installation. To remove settings and state as well, run:

```bash
rm -rf ~/.config/deskally ~/.local/state/deskally
```

## Development

Run the source version and the test suite with:

```bash
python3 -m deskally
python3 -m unittest discover -s tests -v
```

Main directories:

- `deskally/`: GTK interface, collectors, configuration, translations, and theme code
- `scripts/`: unified terminal command
- `assets/`: application icon and `.desktop` template
- `tests/`: core unit tests that run without network access
- `docs/`: GitHub preview image

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## License

DeskALLY is released under the [MIT License](LICENSE).
