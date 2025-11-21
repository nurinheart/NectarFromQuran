#!/usr/bin/env python3
"""Test Arabic RIGHT alignment with visual markers"""

import sys
sys.path.insert(0, '/Users/rafathamaan/Documents/NectarFromQuran')

from cairo_renderer import CairoArabicRenderer
from PIL import Image, ImageDraw

# Test Arabic text
arabic_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

# Create renderer
renderer = CairoArabicRenderer(width=1080, height=600)

# Render with RIGHT alignment
img = renderer.render_arabic_verse(
    text=arabic_text,
    font_family='Amiri',
    font_size=80,
    bg_color=(240, 240, 240),
    text_color=(0, 0, 0),
    max_width=880,
    line_height=1.8,
    align='right',
    transparent_bg=False
)

# Add visual markers to see alignment
draw = ImageDraw.Draw(img)

# Draw vertical lines to show the layout box boundaries
padding = 100
box_left = padding
box_right = 1080 - padding

# Left boundary (green)
draw.line([(box_left, 0), (box_left, 600)], fill='green', width=3)
# Right boundary (red)
draw.line([(box_right, 0), (box_right, 600)], fill='red', width=3)
# Center line (blue)
draw.line([(540, 0), (540, 600)], fill='blue', width=1)

img.save('test_alignment.png')
print("✅ Saved test_alignment.png")
print(f"Green line = LEFT boundary of layout box ({box_left}px)")
print(f"Red line = RIGHT boundary of layout box ({box_right}px)")
print(f"Blue line = CENTER of image (540px)")
print(f"\nFor RIGHT alignment, Arabic text should:")
print(f"  1. Start near the RED line (right edge)")
print(f"  2. Flow LEFTWARD from there")
print(f"  3. NOT be centered between green and red lines")
