"""Small built-in Turkish and English translation table."""

from __future__ import annotations


SUPPORTED_LANGUAGES = ("tr", "en")

STRINGS = {
    "tr": {
        "settings_title": "DeskALLY Ayarları",
        "cancel": "İptal",
        "save": "Kaydet",
        "panel_name": "Panel adı",
        "language": "Dil",
        "countdown_day": "Kronometre günü",
        "countdown_time": "Kronometre saati",
        "panel_color": "Panel rengi",
        "color_picker_title": "DeskALLY rengini seç",
        "panel_width": "Panel genişliği",
        "city": "Şehir",
        "city_placeholder": "Boş bırakırsan otomatik bulunur",
        "city_tooltip": "Otomatik konum çalışmazsa şehir adını buraya yazabilirsin",
        "show_countdown": "Geri sayımı göster",
        "show_wan": "WAN IP adresini göster",
        "show_local_ip": "Yerel IP adresini göster",
        "show_city": "Şehir bilgisini göster",
        "keep_above": "Diğer pencerelerin üstünde tut",
        "tip": "İpucu: Paneli sol tuşla tutup sürükle. Menüyü sağ tıkla aç.",
        "network": "AĞ",
        "system": "SİSTEM",
        "settings_tooltip": "Panel ayarları",
        "menu_refresh": "Şimdi yenile",
        "menu_settings": "Ayarlar",
        "menu_reset": "Konumu sıfırla",
        "menu_about": "Hakkında",
        "menu_quit": "Kapat",
        "updated": "Son yenileme",
        "about": "Linux masaüstü için sürüklenebilir sistem ve ağ paneli.",
    },
    "en": {
        "settings_title": "DeskALLY Settings",
        "cancel": "Cancel",
        "save": "Save",
        "panel_name": "Panel name",
        "language": "Language",
        "countdown_day": "Countdown date",
        "countdown_time": "Countdown time",
        "panel_color": "Panel color",
        "color_picker_title": "Choose the DeskALLY color",
        "panel_width": "Panel width",
        "city": "City",
        "city_placeholder": "Leave empty for automatic detection",
        "city_tooltip": "Enter a city here if automatic location detection fails",
        "show_countdown": "Show countdown",
        "show_wan": "Show WAN IP address",
        "show_local_ip": "Show local IP address",
        "show_city": "Show city",
        "keep_above": "Keep above other windows",
        "tip": "Tip: Hold the left mouse button to drag. Right-click to open the menu.",
        "network": "NETWORK",
        "system": "SYSTEM",
        "settings_tooltip": "Panel settings",
        "menu_refresh": "Refresh now",
        "menu_settings": "Settings",
        "menu_reset": "Reset position",
        "menu_about": "About",
        "menu_quit": "Quit",
        "updated": "Last updated",
        "about": "A draggable system and network panel for Linux desktops.",
    },
}


def text(language: str, key: str) -> str:
    language = language if language in SUPPORTED_LANGUAGES else "tr"
    return STRINGS[language][key]
