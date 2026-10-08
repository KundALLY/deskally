#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
app_dir="$HOME/.local/share/deskally"
bin_dir="$HOME/.local/bin"
libexec_dir="$HOME/.local/libexec"
applications_dir="$HOME/.local/share/applications"
autostart_dir="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
icons_dir="$HOME/.local/share/icons/hicolor/scalable/apps"

if ! python3 -c 'import gi; gi.require_version("Gtk", "3.0"); from gi.repository import Gtk' 2>/dev/null; then
  echo "Missing dependencies. Run this first:" >&2
  echo "  sudo apt install python3-gi gir1.2-gtk-3.0" >&2
  exit 1
fi

# Eski KundALLY Panel sürecini yeni DeskALLY kurulmadan önce kapat.
if [[ -x "$bin_dir/kundally-panel" ]]; then
  "$bin_dir/kundally-panel" stop >/dev/null 2>&1 || true
fi

install -d "$app_dir" "$bin_dir" "$libexec_dir" "$applications_dir" "$autostart_dir" "$icons_dir"
rm -rf "$app_dir/deskally"
cp -a "$project_dir/deskally" "$app_dir/"
install -Dm644 "$project_dir/LICENSE" "$app_dir/LICENSE"
install -Dm755 "$project_dir/scripts/deskally" "$bin_dir/deskally"
install -Dm644 "$project_dir/assets/deskally.svg" "$icons_dir/deskally.svg"

cat >"$libexec_dir/deskally-app" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="$app_dir\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m deskally "\$@"
EOF
chmod 755 "$libexec_dir/deskally-app"

sed "s|@HOME@|$HOME|g" "$project_dir/assets/deskally.desktop.in" \
  >"$applications_dir/deskally.desktop"
cp "$applications_dir/deskally.desktop" "$autostart_dir/deskally.desktop"
chmod 644 "$applications_dir/deskally.desktop" "$autostart_dir/deskally.desktop"

# Eski marka ve 0.x sürümlerinden kalan çalıştırıcıları kaldır.
rm -rf "$HOME/.local/share/kundally-panel"
rm -f "$bin_dir/kundally-panel" "$libexec_dir/kundally-panel-app" \
  "$bin_dir/kundally-panelctl" "$bin_dir/kundally-panel-theme" \
  "$bin_dir/panel-renk" "$bin_dir/panel-turkuaz" "$bin_dir/panel-mavi" \
  "$bin_dir/panel-kirmizi" "$bin_dir/panel-yesil" "$bin_dir/panel-mor" \
  "$bin_dir/panel-altin"
rm -f "$applications_dir/kundally-panel.desktop" "$autostart_dir/kundally-panel.desktop" \
  "$icons_dir/kundally-panel.svg"

command -v update-desktop-database >/dev/null && update-desktop-database "$applications_dir" || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true

if [[ "${1:-}" != "--no-start" ]]; then
  "$bin_dir/deskally" restart
fi

echo "Installation complete. Look for 'DeskALLY' in the application menu."
