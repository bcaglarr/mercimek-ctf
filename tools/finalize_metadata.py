#!/usr/bin/env python3
"""
Mercimek ve G4 Paniği - metadata ve Flag 1 yerleştirme.

Adımlar (piksellere dokunmaz):
  1) exiftool ile orijinalin metadata'sını kopyala, LensMake / LensModel yaz
     (Flag 2 -> Windows Özellikler > Ayrıntılar > "Mercek modeli").
  2) exiftool C2PA (APP11/JUMBF) bloklarını düşürdüyse orijinalden geri ekle.
  3) EN SON: SOI'nin hemen arkasına ham bir APP15 (FFEF) segmenti ekle;
     içinde Flag 1 ve ASCII kedi var -> Not Defteri'nde ilk satırlarda görünür.
     (exiftool her yazışta bu segmenti silebileceği için en son eklenir.)

Kullanım:
  python3 finalize_metadata.py orijinal.jpg bilet.jpg cikti.jpg
Gereksinim: exiftool
"""
import shutil, struct, subprocess, sys

ORIG, TICKET, DST = sys.argv[1:4]
FLAG1 = b"ETUSEC={burada_oldugunu_mu_dusundun_ayrintilara_bakmalisin}"
FLAG2 = "ETUSEC={sacmalama_cantadaki_bilete_baksana}"
CAT = b" /\\_/\\\r\n( o.o )\r\n > ^ <"


def segments(data):
    """SOS'a kadar olan JPEG segmentlerini (marker, başlangıç, bitiş) döndürür."""
    i, out = 2, []
    while data[i + 1] != 0xDA:
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        out.append((data[i + 1], i, i + 2 + length))
        i += 2 + length
    return out


shutil.copy(TICKET, DST)
subprocess.run(["exiftool", "-q", "-overwrite_original", "-TagsFromFile", ORIG,
                "-all:all", DST], check=True)
subprocess.run(["exiftool", "-q", "-overwrite_original",
                "-Artist=", "-XPAuthor=", "-Comment=", "-UserComment=", "-XPComment=",
                "-LensMake=Sirkeci", f"-LensModel={FLAG2}", DST], check=True)

data = open(DST, "rb").read()
data = data[:data.rfind(b"\xff\xd9") + 2]            # sondaki artıkları temizle

if b"jumb" not in data:                               # C2PA'yı geri ekle
    orig = open(ORIG, "rb").read()
    app11 = b"".join(orig[s:e] for m, s, e in segments(orig) if m == 0xEB)
    pos = next(s for m, s, e in segments(data) if not 0xE0 <= m <= 0xEF)
    data = data[:pos] + app11 + data[pos:]

payload = b"\r\n\r\n" + FLAG1 + b"\r\n\r\n" + CAT + b"\r\n\r\n"
app15 = b"\xff\xef" + struct.pack(">H", len(payload) + 2) + payload
data = data[:2] + app15 + data[2:]
open(DST, "wb").write(data)
print("Flag 1 konumu:", data.find(FLAG1), "adet:", data.count(FLAG1))
