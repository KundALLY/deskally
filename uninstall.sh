#!/usr/bin/env bash
set -euo pipefail

"$HOME/.local/bin/deskally" stop 2>/dev/null || true
"$HOME/.local/bin/kundally-panel" stop 2>/dev/null || true
rm -rf "$HOME/.local/share/deskally" "$HOME/.local/share/kundally-panel"
rm -f "$HOME/.local/bin/deskally" "$HOME/.local/bin/kundally-panel" \
  "$HOME/.local/libexec/deskally-app" "$HOME/.local/libexec/kundally-panel-app"
rm -f "$HOME/.local/share/applications/deskally.desktop" \
  "$HOME/.local/share/applications/kundally-panel.desktop"
rm -f "${XDG_CONFIG_HOME:-$HOME/.config}/autostart/deskally.desktop" \
  "${XDG_CONFIG_HOME:-$HOME/.config}/autostart/kundally-panel.desktop"
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/deskally.svg" \
  "$HOME/.local/share/icons/hicolor/scalable/apps/kundally-panel.svg"

echo "DeskALLY removed. Personal settings have been preserved."
