# 🐾 Mercimek ve G4 Paniği

<p align="center"><img src="docs/images/challenge_preview.jpg" width="300" alt="Mercimek metroda"></p>

| | |
|---|---|
| **Kategori** | Forensics / Steganografi |
| **Zorluk** | Kolay – Orta (3 aşamalı) |
| **Flag sayısı** | 3 |
| **Flag formatı** | `ETUSEC{....}` (dosyada `ETUSEC={...}` biçiminde yazılı) |
| **Etkinlik** | ETUSEC CTF |
| **Site** | https://mercimek-ctf.vercel.app/ |

## 📖 Hikâye

G4 otobüsü yine tıklım tıklım. Bizim kedi Mercimek derse yetişmeye çalışıyor. Kalabalıktan dışarıyı göremiyor. "Hangi durakta inecektim, yoksa geçtik mi?" diye paniklemeye başlıyor.
🕵️‍♂️ Mercimek'e yardım et!
Bu dosyada saklı 3 farklı flag var. Önce dosyanın derinliklerine in, sonra çantasındaki o gizli bileti ortaya çıkar ve onu doğru durakta indir! 🐾
( Flag formatı: ETUSEC{....} )

## 📁 Klasör yapısı

```
challenge/challenge.jpg   Yarışmacılara verilen dosya (bayt bayt orijinal)
site/                     Statik tanıtım sayfası (Vercel)
tools/                    Soruyu üretmek için kullanılan betikler
docs/images/              Çözüm görselleri
WRITEUP.md                Adım adım çözüm (SPOILER!)
```

## 🚀 Çalıştırma

**Yarışmacı olarak:** `challenge/challenge.jpg` dosyasını indir ve incele. Ekran görüntüsü alma, dosyanın kendisiyle çalış.

**Siteyi yerelde açmak:**
```bash
cd site
cp ../challenge/challenge.jpg .
python3 -m http.server 8000      # http://localhost:8000
```
Vercel'e yayınlamak için `site/` klasörünü (içine `challenge.jpg` koyarak) build adımı olmadan statik proje olarak deploy et.

**Soruyu yeniden üretmek:**
```bash
pip install -r tools/requirements.txt      # + exiftool kurulu olmalı
python3 tools/build_ticket.py orijinal.jpg bilet.jpg
python3 tools/finalize_metadata.py orijinal.jpg bilet.jpg challenge.jpg
python3 tools/bitplanes.py challenge.jpg out/   # kontrol: out/B3.png
```
> Not: Dosyayı başka bir programla yeniden kaydetmek (yeniden sıkıştırmak) gizli bileti bozar.

## 🙌 Emeği geçenler

- **Soru yazarı:** Bağdagül Çağlar ([@bcaglarr](https://github.com/bcaglarr))
- **Etkinlik:** ETUSEC CTF
- **Araçlar:** Python (Pillow, NumPy), exiftool, Aperi'Solve
- Kedi görseli yapay zekâ ile üretilmiştir (dosyada C2PA bilgisi bulunur).

## 📄 Lisans

MIT – ayrıntılar için [LICENSE](LICENSE).
