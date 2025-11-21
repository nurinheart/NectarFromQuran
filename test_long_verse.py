"""
Test script to generate slides for the longest verse (2:282)
"""
from generate_post_cairo import QuranPostGeneratorCairo
from quran_api import QuranAPI
from config import DEFAULT_THEME

def test_longest_verse():
    """Test with verse 2:282 - the longest verse in the Quran"""
    api = QuranAPI()
    generator = QuranPostGeneratorCairo(theme_name=DEFAULT_THEME)
    
    print("🔍 Fetching verse 2:282 (longest verse in Quran)...")
    verse_data = api.get_verse(2, 282)
    
    if verse_data:
        print(f"✅ Fetched verse 2:282")
        print(f"📏 Arabic length: {len(verse_data['arabic'])} characters")
        print(f"📏 Translation length: {len(verse_data['translation'])} characters")
        
        # Add tafsir and example
        verse_data['tafsir'] = "This is the longest verse in the Quran, known as the 'Verse of Debt' (Ayat al-Dayn). It emphasizes the importance of documenting financial transactions in writing with witnesses. This protects both the creditor and debtor, prevents disputes, and establishes clear evidence. The verse shows Islam's attention to practical matters and financial justice, teaching believers to be meticulous in their dealings while maintaining trust in Allah."
        verse_data['example'] = "When entering into financial agreements, always document them clearly with witnesses. This protects all parties and prevents future disputes. Even among friends or family, written agreements show wisdom and prevent misunderstandings."
        
        print(f"📏 Tafsir length: {len(verse_data['tafsir'])} characters")
        
        print("\n📖 Generating slides...")
        filenames = generator.generate_post(verse_data)
        
        print(f"\n✅ Generated {len(filenames)} slides total!")
        print(f"📁 Check output folder for: quran_post_*_slide*.png")
    else:
        print("❌ Failed to fetch verse")

if __name__ == "__main__":
    test_longest_verse()
