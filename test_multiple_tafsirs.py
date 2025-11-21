import requests
import json

def test_tafsir(surah, ayah):
    """Test tafsir lengths for a specific verse"""
    url = f"https://quranapi.pages.dev/api/tafsir/{surah}_{ayah}.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n{'='*80}")
        print(f"VERSE: {data.get('surahName', '')} ({surah}:{ayah})")
        print('='*80)
        
        for tafsir in data.get('tafsirs', []):
            author = tafsir.get('author', 'Unknown')
            content = tafsir.get('content', '')
            length = len(content)
            
            print(f"\n{author}")
            print(f"  Length: {length:,} characters")
            print(f"  Preview: {content[:200]}...")
            
    except Exception as e:
        print(f"Error fetching {surah}:{ayah}: {e}")

# Test with various verses
print("Testing Tazkirul Quran consistency across different verses:\n")

# Short verse
test_tafsir(112, 1)  # Qul huwa Allahu ahad

# Medium verse  
test_tafsir(55, 4)   # He taught him eloquent speech

# Long verse
test_tafsir(2, 282)  # Longest verse in Quran (debt recording)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("If Tazkirul Quran consistently provides:")
print("  ✅ Verse-specific explanations")
print("  ✅ ~1000-2000 char length")
print("  ✅ Meaningful content")
print("\nThen it's the PERFECT choice for Instagram format!")
