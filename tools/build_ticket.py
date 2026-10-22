#!/usr/bin/env python3
"""
Mercimek ve G4 Paniği - gizli bilet üretici (Flag 3).

Orijinal görseldeki krem rengi çantanın üzerine, yalnızca MAVİ kanalın
3. bitinde (değer 8) görünen bir "bilet" çizer.

Yöntem:
  * Bilet dikdörtgeninin içindeki her pikselin mavi değeri, en yakın
    "hedef" değere taşınır: yazı/çerçeve pikselleri için bit3 = 1,
    arka plan için bit3 = 0.
  * Hedef değerler v % 8 ∈ {2..5} aralığından seçilir; böylece JPEG
    sıkıştırmasının ±2 civarı yuvarlama hatası biti çevirmez.
  * Ortalama değişim ~2.6 seviye, en fazla 6 seviyedir; kumaş dokusu
    korunduğu için normal bakışta bilet görünmez.
  * Çıktı JPEG kalite 100, 4:4:4 (kroma alt örneklemesi yok) kaydedilir.

Kullanım:
  python3 build_ticket.py girdi.jpg cikti.jpg
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC, DST = sys.argv[1], sys.argv[2]
FLAG3_L1 = "ETUSEC={hazirlan_mercimek_"
FLAG3_L2 = "bir_durak_sonra_iniyoruz_:3}"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
BIT = 3                                   # gizlenen bit düzlemi
x0, y0, x1, y1 = 655, 1290, 950, 1460     # biletin çantadaki konumu (piksel)

im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(int)

# 1) Bilet maskesini çiz (255 = yazı/çerçeve)
m = Image.new("L", im.size, 0)
d = ImageDraw.Draw(m)
f1, f2, f3 = (ImageFont.truetype(FONT, s) for s in (24, 18, 17))
d.rectangle([x0, y0, x1, y1], outline=255, width=3)
d.line([x0 + 8, y0 + 40, x1 - 8, y0 + 40], fill=255, width=2)
d.text((x0 + 111, y0 + 8), "BILET", font=f1, fill=255)
d.text((x0 + 10, y0 + 50), "Yolcu: Mercimek", font=f2, fill=255)
d.text((x0 + 8, y0 + 88), FLAG3_L1, font=f3, fill=255)
d.text((x0 + 8, y0 + 118), FLAG3_L2, font=f3, fill=255)
mask = np.array(m) > 127

# 2) Bölgedeki mavi değerleri en yakın uygun hedefe taşı
X0, Y0, X1, Y1 = x0 - 6, y0 - 6, x1 + 7, y1 + 7
B = a[Y0:Y1, X0:X1, 2]
want = mask[Y0:Y1, X0:X1].astype(int)
vals = np.arange(256)
safe = (vals % 8 >= 2) & (vals % 8 <= 5)          # JPEG'e dayanıklı değerler
new = np.zeros_like(B)
for w in (0, 1):
    c = vals[safe & (((vals >> BIT) & 1) == w)]
    idx = np.abs(B[..., None] - c[None, None, :]).argmin(-1)
    new = np.where(want == w, c[idx], new)
a[Y0:Y1, X0:X1, 2] = new
print(f"ortalama |ΔB| = {np.abs(new - B).mean():.2f}, en fazla = {np.abs(new - B).max()}")

# 3) Kaydet ve doğrula
Image.fromarray(np.clip(a, 0, 255).astype("uint8")).save(DST, quality=100, subsampling=0)
t = np.array(Image.open(DST)).astype(int)
err = int((((t[Y0:Y1, X0:X1, 2] >> BIT) & 1) != want).sum())
print(f"JPEG sonrası hatalı bit: {err} / {want.size}")
