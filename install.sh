#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
app_dir="$HOME/.local/share/kundally-panel"
bin_dir="$HOME/.local/bin"
applications_dir="$HOME/.local/share/applications"
autostart_dir="${XDG_CONFIG_HOME:-$HOME/.config}/autostart"
icons_dir="$HOME/.local/share/icons/hicolor/scalable/apps"

if ! python3 -c 'import gi; gi.require_version("Gtk", "3.0"); from gi.repository import Gtk' 2>/dev/null; then
  echo "Eksik paketler var. Önce şunu çalıştır:" >&2
  echo "  sudo apt install python3-gi gir1.2-gtk-3.0" >&2
  exit 1
fi

install -d "$app_dir" "$bin_dir" "$applications_dir" "$autostart_dir" "$icons_dir"
rm -rf "$app_dir/kundally_panel"
cp -a "$project_dir/kundally_panel" "$app_dir/"
install -Dm644 "$project_dir/LICENSE" "$app_dir/LICENSE"
install -Dm755 "$project_dir/scripts/kundally-panelctl" "$bin_dir/kundally-panelctl"
install -Dm644 "$project_dir/assets/kundally-panel.svg" "$icons_dir/kundally-panel.svg"

cat >"$bin_dir/kundally-panel" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="$app_dir\${PYTHONPATH:+:\$PYTHONPATH}"
exec python3 -m kundally_panel "\$@"
EOF
chmod 755 "$bin_dir/kundally-panel"

sed "s|@HOME@|$HOME|g" "$project_dir/assets/kundally-panel.desktop.in" \
  >"$applications_dir/kundally-panel.desktop"
cp "$applications_dir/kundally-panel.desktop" "$autostart_dir/kundally-panel.desktop"
chmod 644 "$applications_dir/kundally-panel.desktop" "$autostart_dir/kundally-panel.desktop"

command -v update-desktop-database >/dev/null && update-desktop-database "$applications_dir" || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" >/dev/null 2>&1 || true

if [[ "${1:-}" != "--no-start" ]]; then
  "$bin_dir/kundally-panelctl" restart
fi

echo "Kurulum tamamlandı. Uygulama menüsünde 'KundALLY Panel' diye arayabilirsin."
