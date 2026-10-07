# KundALLY Panel

[Türkçe](README.md) · [English](README.en.md)

![KundALLY Panel önizlemesi](docs/preview.svg)

KundALLY Panel, Linux masaüstünde temel sistem ve ağ bilgilerini küçük bir pencerede gösteren açık kaynaklı bir GTK 3 uygulamasıdır. Amacı CPU, GPU, RAM, IP adresleri, şehir, tarih, saat ve kişisel geri sayımı masaüstünde tek bakışta erişilebilir tutmaktır.

Panel başlık çubuğu kullanmaz. Fareyle doğrudan sürüklenir, son konumunu hatırlar ve görünmesini istemediğin satırları kapattığında boyunu otomatik ayarlar. Arayüz Türkçe ve İngilizce kullanılabilir.

## Özellikler

- CPU kullanımı ve sıcaklığı, GPU sıcaklığı, RAM kullanımı ve yüzdesi
- Etkin ağ arayüzü, yerel IP, genel WAN IP ve yaklaşık şehir bilgisi
- Takvim ve saatle ayarlanabilen kişisel geri sayım
- Türkçe ve İngilizce arayüz, tarih ve geri sayım metni
- Değiştirilebilir panel adı, vurgu rengi ve genişlik
- WAN IP, yerel IP, şehir ve geri sayım satırlarını ayrı ayrı gösterme
- Otomatik bulunamazsa şehri elle belirleme
- Fareyle sürükleme, konumu hatırlama ve sağ tık menüsü
- Oturum açılışında otomatik başlatma
- Tek bir `kundally-panel` komutu altında yönetim
- Kullanıcı dizinine kurulum; yönetici yetkisi gerektirmez

## Desteklenen sistemler

Uygulama Debian, Ubuntu, Linux Mint ve GTK 3 kullanan benzer Linux dağıtımlarını hedefler. X11 masaüstlerinde çalışır. Wayland oturumlarında pencere konumlandırma ve her zaman üstte tutma davranışı masaüstü ortamına göre değişebilir.

## Gereksinimler

Debian ve türevlerinde gerekli paketleri kur:

```bash
sudo apt install python3 python3-gi gir1.2-gtk-3.0
```

Sıcaklık sensörlerinin daha geniş donanım desteği için isteğe bağlı paket:

```bash
sudo apt install lm-sensors
```

## Kurulum

GitHub sayfasında **Code → Download ZIP** ile projeyi indirip arşivi çıkarabilir veya depoyu klonlayabilirsin. Depo yayımlanırken aşağıdaki örnek adresteki `KULLANICI_ADI` alanı gerçek GitHub kullanıcı adıyla değiştirilecektir:

```bash
git clone https://github.com/KULLANICI_ADI/kundally-panel.git
cd kundally-panel
./install.sh
```

Kurucu dosyaları `~/.local` altına kopyalar, uygulama menüsü ve otomatik başlatma kaydı oluşturur, ardından paneli açar. `~/.local/bin` PATH içinde değilse oturumu kapatıp yeniden açmak gerekebilir.

Paneli hemen başlatmadan kurmak için:

```bash
./install.sh --no-start
```

## İlk kullanım

1. Paneli taşımak için herhangi bir boş noktasında sol tuşa basılı tutup sürükle.
2. Ayarları açmak için sağ üstteki **⚙** düğmesine bas.
3. **Dil** listesinden **Türkçe** veya **English** seç.
4. Panel adını, rengi, genişliği, geri sayım tarihini ve görünür satırları ayarla.
5. **Kaydet** düğmesine bas. Değişiklikler hemen uygulanır.
6. Yenileme, konumu sıfırlama ve kapatma seçenekleri için panele sağ tıkla.

## Komut kılavuzu

| Komut | Görevi |
| --- | --- |
| `kundally-panel start` | Paneli başlatır. Zaten çalışıyorsa ikinci kopya açmaz. |
| `kundally-panel stop` | Çalışan paneli kapatır. |
| `kundally-panel restart` | Paneli kapatıp güncel ayarlarla yeniden başlatır. |
| `kundally-panel status` | Panelin çalışıp çalışmadığını ve PID değerini gösterir. |
| `kundally-panel logs` | Son 100 günlük satırını gösterir. |
| `kundally-panel color RENK` | Vurgu rengini değiştirip paneli yeniden başlatır. |
| `kundally-panel version` | Kurulu sürüm numarasını gösterir. |
| `kundally-panel help` | Tüm komutların kısa yardımını gösterir. |

Türkçe komut eş adları da bulunur: `baslat`, `durdur`, `yenile`, `durum`, `gunluk`, `renk`, `surum` ve `yardim`.

### Renk komutu

Hazır renkler Türkçe veya İngilizce adla kullanılabilir:

```bash
kundally-panel color turkuaz
kundally-panel color mavi
kundally-panel color kirmizi
kundally-panel color yesil
kundally-panel color mor
kundally-panel color altin
```

İngilizce eşleri `cyan`, `blue`, `red`, `green`, `purple` ve `gold` şeklindedir. Özel bir renk için altı haneli HEX değeri kullan:

```bash
kundally-panel color '#ff8800'
```

Renk komutu başlık, dil, sayaç ve görünürlük gibi diğer ayarları korur.

## Paneldeki bilgiler

| Etiket | Anlamı |
| --- | --- |
| `WAN` | İnternette görünen genel IP adresi |
| `IF` | Varsayılan ağ arayüzü, örneğin `enp10s0` veya `wlan0` |
| `IP` | Yerel ağdaki IPv4 adresi |
| `LOC` | Genel IP üzerinden yaklaşık şehir veya elle girilen şehir |
| `CPU` | İşlemci kullanımı ve bulunabiliyorsa sıcaklığı |
| `GPU` | Bulunabiliyorsa ekran kartı sıcaklığı |
| `RAM` | Kullanılan/toplam bellek ve kullanım yüzdesi |

`—` işareti, o bilginin donanımdan ya da sistemden alınamadığını gösterir.

## Ayarlar

- **Panel adı:** Üst bölümde görünen kişisel başlık.
- **Dil:** Türkçe veya İngilizce. Seçim kaydedildiğinde panel, menü ve sonraki ayar penceresi çevrilir.
- **Kronometre günü ve saati:** Geri sayımın ulaşacağı tarih ve saat.
- **Panel rengi:** Renk seçiciyle vurgu rengini değiştirir.
- **Panel genişliği:** 160–420 piksel arasında ayarlanır.
- **Şehir:** Boşsa otomatik bulunur; bir değer yazılırsa `LOC` satırında o değer kullanılır.
- **Görünürlük seçenekleri:** Geri sayım, WAN IP, yerel IP ve şehir ayrı ayrı kapatılabilir.
- **Diğer pencerelerin üstünde tut:** Masaüstü ortamı destekliyorsa paneli önde tutar.

## Dosya konumları

| Konum | İçerik |
| --- | --- |
| `~/.local/share/kundally-panel/` | Kurulu uygulama dosyaları |
| `~/.local/bin/kundally-panel` | Kullanıcı komutu |
| `~/.local/share/applications/kundally-panel.desktop` | Uygulama menüsü kaydı |
| `~/.config/autostart/kundally-panel.desktop` | Otomatik başlatma kaydı |
| `~/.config/kundally-panel/config.json` | Kullanıcı ayarları |
| `~/.local/state/kundally-panel/` | PID, konum ve günlük dosyaları |

## Gizlilik ve ağ kullanımı

Yerel IP ve sistem değerleri bilgisayarda okunur. WAN IP açıksa panel sırasıyla Cloudflare Trace, ipify, ident.me veya ifconfig.me hizmetlerinden birine kısa bir istek gönderebilir. Şehir açıksa ipinfo.io, ipapi.co, ipwho.is veya ip-api.com kaynaklarından biri kullanılabilir.

Bu hizmetler isteği gönderen genel IP adresini doğal olarak görür. WAN IP ve şehir satırları ayarlardan ayrı ayrı kapatılabilir. Şehir alanına elle değer girildiğinde şehir sorgusu yapılmaz.

## Sorun giderme

Panel açılmıyorsa önce durum ve günlükleri kontrol et:

```bash
kundally-panel status
kundally-panel logs
kundally-panel restart
```

`kundally-panel: command not found` hatasında `~/.local/bin` dizininin PATH içinde olduğundan emin ol veya şu tam yolu kullan:

```bash
~/.local/bin/kundally-panel restart
```

Şehir görünmüyorsa internet bağlantısını kontrol et veya **Ayarlar → Şehir** alanına adı elle yaz. Sıcaklık `—` görünüyorsa `lm-sensors` kurup sistemin sensör desteğini denetle. Bir satır ayarlarda açık olduğu halde görünmüyorsa paneli `kundally-panel restart` ile yeniden başlat. Panel ekran dışında kaldıysa sağ tık menüsünden **Konumu sıfırla** seçeneğini kullan.

## Güncelleme

Yeni kaynak kodunu indirdikten sonra proje dizininde kurucuyu yeniden çalıştır:

```bash
./install.sh
```

Kişisel ayarlar ve panel konumu korunur.

## Kaldırma

Proje dizininde:

```bash
./uninstall.sh
```

Kaldırıcı uygulamayı, komutu, menü kaydını ve otomatik başlatmayı siler. Kişisel ayar dosyasını daha sonra yeniden kurabilmen için korur. Ayarları da silmek istersen ayrıca şunu çalıştır:

```bash
rm -rf ~/.config/kundally-panel ~/.local/state/kundally-panel
```

## Geliştirme

Kaynak koddan çalıştırmak ve testleri yürütmek için:

```bash
python3 -m kundally_panel
python3 -m unittest discover -s tests -v
```

Ana dizinler:

- `kundally_panel/`: GTK arayüzü, veri toplayıcılar, yapılandırma, çeviriler ve tema kodu
- `scripts/`: birleşik terminal komutu
- `assets/`: uygulama simgesi ve `.desktop` şablonu
- `tests/`: ağ kullanmadan çalışan temel birim testleri
- `docs/`: GitHub önizleme görseli

Katkı süreci için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## Lisans

KundALLY Panel [MIT Lisansı](LICENSE) ile yayımlanır.
