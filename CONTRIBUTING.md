# Katkı / Contributing

## Türkçe

Hata bildirirken dağıtımını, masaüstü ortamını, X11 veya Wayland kullandığını, sorunu oluşturma adımlarını ve `deskally logs` çıktısındaki ilgili satırları yaz. Genel IP gibi kişisel bilgileri paylaşmadan önce gizle.

Kod katkısı için:

1. Depoyu çatalla ve ayrı bir dal aç.
2. Değişikliği küçük ve tek amaçlı tut.
3. Kullanıcıya görünen yeni metni `deskally/i18n.py` içinde Türkçe ve İngilizce ekle.
4. `python3 -m unittest discover -s tests -v` komutunu çalıştır.
5. Değişikliğin amacı ve doğrulama adımlarıyla bir pull request aç.

## English

When reporting a bug, include your distribution, desktop environment, X11 or Wayland session, reproduction steps, and relevant lines from `deskally logs`. Remove personal information such as public IP addresses before posting.

For code contributions:

1. Fork the repository and create a focused branch.
2. Keep the change small and limited to one purpose.
3. Add all new user-facing text in both Turkish and English in `deskally/i18n.py`.
4. Run `python3 -m unittest discover -s tests -v`.
5. Open a pull request explaining the purpose and validation steps.
