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

## Lisans

Bu proje `GPL-3.0-or-later` yaklaşımıyla paylaşılmaktadır.

Uygulama `PyQt5` kullandığı için lisans notu özellikle buna uyumlu olacak şekilde düzenlenmiştir. Ayrıntılar için kök dizindeki [LICENSE](LICENSE) dosyasına bakabilirsiniz.
