#!/usr/bin/env python3
"""Test script to generate specific verses - including sajdah verses"""

import sys
from generate_post_cairo import QuranPostGeneratorCairo
from config import DEFAULT_THEME
from quran_api import QuranAPI

def generate_specific_verse(surah, ayah):
    """Generate post for a specific verse"""
    api = QuranAPI()
    verse_data = api.get_verse(surah, ayah)
    
    if not verse_data:
        print(f"❌ Failed to fetch verse {surah}:{ayah}")
        return
    
    # Add dummy theme and tafsir for testing
    verse_data['theme'] = 'Knowledge'
    verse_data['tafsir'] = 'This is a test tafsir for verification purposes.'
    
    print(f"\n📖 Generating post for Surah {surah}, Ayah {ayah}")
    print(f"   Surah: {verse_data['surah_name']}")
    print(f"   Arabic preview: {verse_data['arabic'][:80]}...")
    
    # Check for sajdah marker
    if '۩' in verse_data['arabic']:
        print("   ✅ SAJDAH VERSE DETECTED - Sajdah marker ۩ present")
    
    generator = QuranPostGeneratorCairo(theme_name=DEFAULT_THEME)
    
    # Create Arabic slide to test sajdah marker
    arabic_slide = generator.create_slide_arabic(verse_data)
    
    # Create translation slide to test quotes
    translation_slide = generator.create_slide_translation(verse_data)
    
    # Save slides
    from datetime import datetime
    import os
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    filename1 = f"{output_dir}/sajdah_test_{timestamp}_arabic.png"
    arabic_slide.save(filename1, quality=95, optimize=True)
    print(f"✅ Saved Arabic slide: {filename1}")
    
    filename2 = f"{output_dir}/sajdah_test_{timestamp}_translation.png"
    translation_slide.save(filename2, quality=95, optimize=True)
    print(f"✅ Saved Translation slide: {filename2}")
    
    filenames = [filename1, filename2]
    
    print(f"\n🎉 Successfully generated {len(filenames)} slides!")
    print(f"📁 Files: {', '.join(filenames)}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        surah = int(sys.argv[1])
        ayah = int(sys.argv[2])
        generate_specific_verse(surah, ayah)
    else:
        print("Testing with common sajdah verses:")
        print("1. Surah 32:15 (As-Sajdah)")
        print("2. Surah 7:206 (Al-A'raf)")
        print("\nGenerating Surah 32:15...")
        generate_specific_verse(32, 15)
