# CezaMat'ik

CezaMat'ik, ceza süresi ve adli para cezası hesaplamalarını masaüstünde pratik biçimde yapmak için geliştirilen bir `PyQt5` uygulamasıdır.

Uygulama içinde:

- temel ceza hesaplama akışı
- oran bazlı indirim / artırım işlemleri
- dolandırıcılık adli para cezası hesaplama modülü
- yardımcı araçlar penceresi
  - hapsi güne çevirme
  - APC orantılama
  - yaş hesaplama

bulunur.

## Kurulum

Önce bağımlılıkları kurun:

```bash
pip install -r requirements.txt
```

Gerekirse ayrıca:

```bash
pip install requests
```

## Çalıştırma

Uygulamayı proje klasöründe şu komutla başlatabilirsiniz:

```bash
python CezaMatik.py
```

## Proje Yapısı

- `CezaMatik.py`: uygulama giriş noktası
- `ui/`: arayüz bileşenleri ve dialog pencereleri
- `utils/`: hesaplama ve yardımcı işlevler
- `assets/`: görsel dosyalar

## Notlar

- Uygulama `PyQt5` ile geliştirilmiştir.
- Hesaplamalarda hukuk uygulamasına uygun sabit dönüşümler kullanılmaktadır.
- Bazı yardımcı araçlarda `1 yıl = 365 gün` ve `1 ay = 30 gün` kabulü esas alınır.

## Lisans ve Üçüncü Taraf Notları

- Proje lisansı için:
  - `LICENSE`
- Üçüncü taraf bağımlılık ve lisans notları için:
  - `THIRD_PARTY.md`
- Uygulamanın ceza hesaplama mantığı ve yardımcı araçları proje içinde özgün olarak yazılmıştır.
