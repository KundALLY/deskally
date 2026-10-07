#!/usr/bin/env bash
set -euo pipefail

"$HOME/.local/bin/kundally-panelctl" stop 2>/dev/null || true
rm -rf "$HOME/.local/share/kundally-panel"
rm -f "$HOME/.local/bin/kundally-panel" "$HOME/.local/bin/kundally-panelctl" \
  "$HOME/.local/bin/kundally-panel-theme" "$HOME/.local/bin/panel-renk" \
  "$HOME/.local/bin/panel-turkuaz" "$HOME/.local/bin/panel-mavi" \
  "$HOME/.local/bin/panel-kirmizi" "$HOME/.local/bin/panel-yesil" \
  "$HOME/.local/bin/panel-mor" "$HOME/.local/bin/panel-altin"
rm -f "$HOME/.local/share/applications/kundally-panel.desktop"
rm -f "${XDG_CONFIG_HOME:-$HOME/.config}/autostart/kundally-panel.desktop"
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/kundally-panel.svg"

echo "KundALLY Panel kaldırıldı. Kişisel ayarlar korunmuştur."
