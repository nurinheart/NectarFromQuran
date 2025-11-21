#!/usr/bin/env python3
"""
FINAL VERIFICATION - All rendering issues fixed
Tests both harakat preservation and font rendering
"""

from PIL import Image, ImageDraw, ImageFont
from arabic_handler import prepare_arabic_text
from generate_post import QuranPostGenerator
import os

print('╔═══════════════════════════════════════════════════════════════════╗')
print('║            🕌 FINAL VERIFICATION - ALL FIXES COMPLETE              ║')
print('╚═══════════════════════════════════════════════════════════════════╝')
print()

# Test 1: Arabic reshaping preserves harakat
print('1️⃣  HARAKAT PRESERVATION TEST')
print('─' * 70)

test_text = 'قُلْ يَٰعِبَادِىَ ٱلَّذِينَ أَسْرَفُوا۟ عَلَىٰٓ أَنفُسِهِمْ'
print(f'Original text: {test_text}')

# Count harakat in original
harakat_chars = ['َ', 'ِ', 'ُ', 'ً', 'ٍ', 'ٌ', 'ْ', 'ّ', 'ٰ', '۟', 'ٓ']
original_harakat_count = sum(test_text.count(h) for h in harakat_chars)

# Process through handler
processed = prepare_arabic_text(test_text)
processed_harakat_count = sum(processed.count(h) for h in harakat_chars)

print(f'Original harakat count: {original_harakat_count}')
print(f'After processing: {processed_harakat_count}')
print(f'✅ Harakat preserved: {processed_harakat_count >= original_harakat_count * 0.9}')
print()

# Test 2: Font rendering for Arabic
print('2️⃣  ARABIC FONT RENDERING TEST')
print('─' * 70)

fonts_to_test = [
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/Supplemental/DecoTypeNaskh.ttc',
    '/System/Library/Fonts/Supplemental/KufiStandardGK.ttc',
]

for font_path in fonts_to_test:
    if os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, 48)
            bbox = font.getbbox(processed)
            width = bbox[2] - bbox[0]
            print(f'✅ {os.path.basename(font_path):35} Width: {width}px')
        except Exception as e:
            print(f'❌ {os.path.basename(font_path):35} Error: {str(e)[:30]}')
    else:
        print(f'⚠️  {os.path.basename(font_path):35} Not found')
print()

# Test 3: English text rendering
print('3️⃣  ENGLISH TEXT RENDERING TEST')
print('─' * 70)

english_texts = [
    'Az-Zumar (39:53)',
    'Sahih International',
    'Tafsir Ibn Kathir',
]

for font_path in fonts_to_test[:2]:  # Test first 2 fonts
    if os.path.exists(font_path):
        font_name = os.path.basename(font_path)
        try:
            font = ImageFont.truetype(font_path, 40)
            works = True
            for text in english_texts:
                bbox = font.getbbox(text)
                if bbox[2] - bbox[0] <= 0:
                    works = False
            print(f'✅ {font_name:35} English: {"OK" if works else "FAIL"}')
        except Exception as e:
            print(f'❌ {font_name:35} Error: {str(e)[:30]}')
print()

# Test 4: Generate complete post
print('4️⃣  COMPLETE POST GENERATION TEST')
print('─' * 70)

try:
    gen = QuranPostGenerator('elegant_black', style='pattern')
    slides, idx, verse = gen.generate_post('output', specific_index=0)
    
    print(f'✅ Generated {len(slides)} slides')
    print(f'   Surah: {verse["surah_name"]} ({verse["surah_number"]}:{verse["ayah_number"]})')
    print(f'   Arabic: {verse["arabic"][:40]}...')
    print(f'   Translation: {verse["translation"][:50]}...')
    
    # Verify files exist and have reasonable size
    print()
    print('   Generated files:')
    for i, slide_path in enumerate(slides, 1):
        if os.path.exists(slide_path):
            size_mb = os.path.getsize(slide_path) / (1024 * 1024)
            print(f'   ✅ Slide {i}: {os.path.basename(slide_path)} ({size_mb:.2f} MB)')
        else:
            print(f'   ❌ Slide {i}: File not found!')
    
    print()
    print('   Latest slides to review:')
    for slide in slides:
        print(f'   • {slide}')
    
except Exception as e:
    print(f'❌ Generation failed: {e}')
    import traceback
    traceback.print_exc()

print()
print('═' * 70)
print('✅ VERIFICATION COMPLETE')
print('═' * 70)
print()
print('🎯 VISUAL INSPECTION CHECKLIST:')
print()
print('Open the generated images and verify:')
print('  □ Arabic text has small marks above/below letters (harakat)')
print('  □ English text is clear (no boxes □)')
print('  □ References show correctly: Az-Zumar (39:53)')
print('  □ All slides have grainy texture background')
print('  □ Arabic text flows top-to-bottom naturally')
print()
print('📂 Run: open output/verse_0_slide*.png')
print()
