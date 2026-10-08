# Katkı

[English](CONTRIBUTING.md) · [Türkçe](CONTRIBUTING.tr.md)

Hata bildirirken dağıtımını, masaüstü ortamını, X11 veya Wayland kullandığını, sorunu oluşturma adımlarını ve `deskally logs` çıktısındaki ilgili satırları yaz. Genel IP gibi kişisel bilgileri paylaşmadan önce gizle.

Kod katkısı için:

1. Depoyu çatalla ve ayrı bir dal aç.
2. Değişikliği küçük ve tek amaçlı tut.
3. Kullanıcıya görünen yeni metni `deskally/i18n.py` içinde Türkçe ve İngilizce ekle.
4. `python3 -m unittest discover -s tests -v` komutunu çalıştır.
5. Değişikliğin amacı ve doğrulama adımlarıyla bir pull request aç.

