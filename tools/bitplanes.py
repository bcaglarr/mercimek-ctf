#!/usr/bin/env python3
"""
Aperi'Solve / Stegsolve gibi bit düzlemlerini çıkarır: (piksel >> n) & 1.
Kullanım: python3 bitplanes.py challenge.jpg cikti_klasoru/
"""
import os, sys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
a = np.array(Image.open(src).convert("RGB"))
for ci, ch in enumerate("RGB"):
    for n in range(8):
        plane = ((a[..., ci] >> n) & 1) * 255
        Image.fromarray(plane.astype("uint8")).save(f"{out}/{ch}{n}.png")
print("Bitti. Flag 3 için B3.png dosyasına bak.")
