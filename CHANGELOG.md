# Değişiklik günlüğü

## 0.4.1 — 2026-10-08

- Ağ ve sistem satırlarının eski pencere yüksekliği tarafından kesilmesi düzeltildi.
- Panel, açık ayarlara göre içeriğinin doğal yüksekliğine otomatik uzuyor.
- Satırlar açılıp kapatıldığında pencere boyutu anında yeniden hesaplanıyor.
- Kayıtlı konum ekran dışına taşıyorsa görünür alana geri alınıyor.

## 0.4.0 — 2026-10-08

- WAN IP, yerel IP ve şehir görünürlüğü için ayrı ayarlar eklendi.
- Otomatik şehir bulmaya dört IPv4 kaynağı ve yedek yöntem eklendi.
- Şehir adını elle belirleme seçeneği eklendi.
- RAM satırına kullanım yüzdesi eklendi.

## 0.3.0 — 2026-10-08

- Terminalden kullanılabilen altı renk hazır ayarı eklendi.
- Özel renkler için `panel-renk '#RRGGBB'` komutu eklendi.
- Renk değişiminde panelin bütün vurgu tonlarının birlikte değişmesi sağlandı.
- Renk değiştirilirken diğer kullanıcı ayarları korunuyor.

## 0.2.3 — 2026-10-08

- Ağ arayüzünün altında ayrı bir yerel `IP` satırı eklendi.
- Ağ bölümü `WAN`, `IF`, `IP`, `LOC` sırasına getirildi.

## 0.2.2 — 2026-10-08

- Eski panel sürecinin yeni sürümü engellemesi düzeltildi.
- IP satırı daha açık olması için `WAN` yerine `IP` olarak adlandırıldı.
- Yerel IP için `ip`, NetworkManager ve `hostname` yedekleri eklendi.
- Görüntülenen IP sonucu tanılama günlüğüne eklendi.

## 0.2.1 — 2026-10-08

- Dış IP sorgusuna Debian'da çalışan IPv4 `curl` yedeği eklendi.
- Dış IP beklenirken yerel IP'nin hemen gösterilmesi sağlandı.
- IP alınamadığında boş değer yerine açık bağlantı durumu gösteriliyor.

## 0.2.0 — 2026-10-08

- Kronometre için takvim ve saat seçici eklendi.
- Panel adı ve rengi daha kolay değiştirilebilir hâle getirildi.
- Genel IP ve şehir bilgisine yedek veri kaynakları eklendi.

## 0.1.0 — 2026-10-08

- İlk kullanılabilir prototip.
- Fareyle doğrudan sürükleme ve konumu hatırlama.
- CPU, GPU, RAM, ağ arayüzü, genel IP ve şehir bilgisi.
- Yapılandırılabilir geri sayım, başlık, renk ve genişlik.
- Sağ tık menüsü ile ayarlar, yenileme ve konum sıfırlama.
- Kullanıcı düzeyinde kurulum, otomatik başlatma ve kaldırma betikleri.
