"""
Test tafsir length for various ayahs including longest ones
Check if we're losing important context by truncating
"""

import requests
from auto_tafsir_fetcher import AutoTafsirFetcher

# Test with different types of ayahs
test_verses = [
    (2, 255, "Ayat al-Kursi - famous, likely long tafsir"),
    (2, 282, "Longest ayah in Quran (debt transaction)"),
    (9, 122, "Another very long ayah"),
    (4, 176, "Long ayah about inheritance"),
    (2, 196, "Long ayah about Hajj"),
    (3, 7, "Short ayah"),
    (112, 1, "Very short ayah (Al-Ikhlas)"),
]

fetcher = AutoTafsirFetcher()

print("=" * 80)
print("TAFSIR LENGTH ANALYSIS")
print("=" * 80)

for surah, ayah, description in test_verses:
    print(f"\n{'='*80}")
    print(f"📖 Surah {surah}:{ayah} - {description}")
    print("="*80)
    
    # Fetch full tafsir without cache
    try:
        url = f"https://quranapi.pages.dev/api/tafsir/{surah}_{ayah}.json"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Get Ibn Kathir tafsir
        tafsirs = data.get("tafsirs", [])
        ibn_kathir = next((t for t in tafsirs if 'Ibn Kathir' in t.get('author', '')), None)
        
        if ibn_kathir:
            full_text = ibn_kathir.get("content", "")
            
            # Clean it same way as fetcher
            import re
            full_text = re.sub(r'^##\s+', '', full_text, flags=re.MULTILINE)
            full_text = re.sub(r'<[^>]+>', '', full_text)
            full_text = re.sub(r'\s+', ' ', full_text)
            full_text = full_text.strip()
            
            # Get summarized version
            summarized = fetcher.summarize_tafsir(full_text, max_length=400)
            
            print(f"\n📊 Stats:")
            print(f"   Full tafsir length:       {len(full_text):,} characters")
            print(f"   Summarized length:        {len(summarized):,} characters")
            print(f"   Reduction:                {100 - (len(summarized)/len(full_text)*100):.1f}%")
            print(f"   Sentences in full:        ~{full_text.count('.')}")
            print(f"   Sentences in summary:     ~{summarized.count('.')}")
            
            print(f"\n📝 Full Tafsir (first 500 chars):")
            print(f"   {full_text[:500]}...")
            
            print(f"\n✂️  Summarized (what's shown in post):")
            print(f"   {summarized}")
            
            # Check if we're losing critical content
            if len(full_text) > 1000:
                print(f"\n⚠️  WARNING: Full tafsir is {len(full_text):,} chars - we're showing only {len(summarized)/len(full_text)*100:.1f}%")
        else:
            print("❌ Ibn Kathir tafsir not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*80)
print("RECOMMENDATIONS:")
print("="*80)
print("""
If tafsirs are consistently >1000 chars and we're showing <50%, consider:

Option 1: Increase max_length to 600-800 chars
  - Pro: More complete context
  - Con: Might overflow slide if text is small font

Option 2: Split long tafsir into multiple slides (like we do for long verses)
  - Pro: Shows complete tafsir without losing meaning
  - Con: More slides per post

Option 3: Smart summarization - keep first paragraph + key points
  - Pro: Preserves main message
  - Con: Requires more complex logic

Option 4: Keep current 400 chars but ensure it's first complete sentences
  - Pro: Current implementation already does this
  - Con: May miss important details
""")
