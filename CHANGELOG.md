# Changelog

[English](CHANGELOG.md) · [Türkçe](CHANGELOG.tr.md)

## Unreleased

- Default to English while keeping Turkish available in settings.
- Use English documentation by default, with links to Turkish versions.
- Replace promotional artwork with a panel-only preview using example data.
- Use English installer and command-line messages; retain Turkish command aliases.

## 0.7.0 — 2026-10-08

- Rename the project to DeskALLY and the main command to `deskally`.
- Update menu entries, icons, installation paths, and bilingual guides.
- Migrate legacy KundALLY Panel settings and window position automatically.
- Clean up legacy installation files during installation.

## 0.6.0 — 2026-10-08

- Add Turkish and English interface selection for dates, countdowns, settings, menus, and descriptions.
- Add English color aliases and bilingual installation and usage guides.
- Update the example configuration to include all current settings.

## 0.5.0 — 2026-10-08

- Consolidate terminal operations under `kundally-panel`.
- Standardize start, stop, restart, status, logs, and color commands.
- Remove legacy commands and separate the internal launcher from user commands.

## 0.4.1 — 2026-10-08

- Fix clipped network and system rows by resizing to the visible content.
- Recalculate window size when rows are toggled.
- Move saved off-screen positions back into the visible area.

## 0.4.0 — 2026-10-08

- Add separate visibility settings for WAN IP, local IP, and city.
- Add four IPv4 city lookup sources with a fallback method and manual city entry.
- Add RAM usage percentage.

## 0.3.0 — 2026-10-08

- Add six command-line color presets and custom HEX colors.
- Update all accent tones together while preserving other settings.

## 0.2.3 — 2026-10-08

- Add a separate local IP row below the network interface.
- Order network rows as WAN, IF, IP, and LOC.

## 0.2.2 — 2026-10-08

- Fix an old panel process preventing the new version from starting.
- Rename the IP row from WAN to IP for clarity.
- Add local IP fallbacks using ip, NetworkManager, and hostname.
- Log the displayed IP for diagnostics.

## 0.2.1 — 2026-10-08

- Add an IPv4 curl fallback for public IP queries on Debian.
- Show the local IP while waiting for the public IP.
- Show connection status when an IP is unavailable.

## 0.2.0 — 2026-10-08

- Add calendar and time selectors for the countdown.
- Update panel title and color controls.
- Add fallback sources for public IP and city information.

## 0.1.0 — 2026-10-08

- Initial usable prototype with mouse dragging and saved position.
- Display CPU, GPU, RAM, network interface, public IP, and city.
- Add configurable countdown, title, color, and width.
- Add a context menu for settings, refresh, and position reset.
- Add per-user installation, autostart, and removal scripts.
