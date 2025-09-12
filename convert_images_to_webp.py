#!/usr/bin/env python3
"""
Batch convert and compress all PNG/JPG images in static/assets/img and subfolders to WebP format.
Requires: pip install pillow
"""
import os
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'assets', 'img')

for root, _, files in os.walk(IMG_DIR):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            src_path = os.path.join(root, file)
            dst_path = os.path.splitext(src_path)[0] + '.webp'
            try:
                with Image.open(src_path) as im:
                    im.save(dst_path, 'WEBP', quality=80, method=6)
                print(f"Converted: {src_path} -> {dst_path}")
            except Exception as e:
                print(f"Failed: {src_path} ({e})")
print("Done. All images converted to WebP.")
