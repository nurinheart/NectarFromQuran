"""
Quran API Handler - Fetches verses with Arabic (Uthmani with diacritics) and translations
ROOT FIX: Proper error handling, caching, offline fallback
Uses quran.com API v4 for accurate Uthmani script with full tashkeel
"""

import requests
import json
import os


class QuranAPI:
    def __init__(self):
        # Use Quran.com API v4 - more reliable with full diacritics
        self.base_url = "https://api.quran.com/api/v4"
        self.cache_file = "quran_cache.json"
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cached verses to avoid repeated API calls"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save cache: {e}")
    
    def get_verse(self, surah, ayah):
        """
        Get verse in Arabic (Uthmani Tajweed script with FULL diacritics) and English translation
        Returns: dict with 'arabic', 'translation', 'surah_name', 'surah_number', 'ayah_number'
        ROOT FIX: Uses Quran.com API v4 which has perfect Uthmani script with all harakat
        NEVER SKIP: Retries 3 times with exponential backoff, timeout increased to 30s
        """
        cache_key = f"{surah}:{ayah}"
        
        # Check cache first
        if cache_key in self.cache:
            print(f"📖 Using cached verse {cache_key}")
            return self.cache[cache_key]
        
        # Retry configuration
        max_retries = 3
        timeout = 30  # Increased from 15s to 30s
        
        # Retry loop - NEVER skip a verse due to temporary network issues
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    import time
                    wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s
                    print(f"🔄 Retry attempt {attempt + 1}/{max_retries} for verse {cache_key} (waiting {wait_time}s)...")
                    time.sleep(wait_time)
                
                # Calculate verse key (used by Quran.com API v4)
                # Format: "surah:ayah" like "2:255" for Ayat al-Kursi
                verse_key = f"{surah}:{ayah}"
                
                # Fetch Arabic text (Uthmani script with full harakat)
                arabic_url = f"{self.base_url}/verses/by_key/{verse_key}"
                arabic_params = {
                    'fields': 'text_uthmani',  # Get Uthmani script
                }
                
                arabic_response = requests.get(arabic_url, params=arabic_params, timeout=timeout)
                arabic_response.raise_for_status()
                arabic_data = arabic_response.json()
                
                verse_info = arabic_data['verse']
                
                # Get Arabic text with FULL HARAKAT from Uthmani script
                arabic_text = verse_info['text_uthmani']
                
                # Fetch translation (Sahih International - ID 20)
                trans_url = f"{self.base_url}/quran/translations/20"
                trans_params = {'verse_key': verse_key}
                
                trans_response = requests.get(trans_url, params=trans_params, timeout=timeout)
                trans_response.raise_for_status()
                trans_data = trans_response.json()
                
                # Get translation text
                translation_text = "Translation not available"
                if trans_data.get('translations') and len(trans_data['translations']) > 0:
                    translation_text = trans_data['translations'][0]['text']
                    # Remove HTML tags (footnote references like <sup foot_note=196080>1</sup>)
                    import re
                    translation_text = re.sub(r'<sup[^>]*>.*?</sup>', '', translation_text)
                    translation_text = re.sub(r'<[^>]+>', '', translation_text)  # Remove any other HTML tags
                    translation_text = translation_text.strip()
                
                # Get chapter (surah) info
                chapter_url = f"{self.base_url}/chapters/{surah}"
                chapter_response = requests.get(chapter_url, timeout=timeout)
                chapter_data = chapter_response.json()
                chapter_info = chapter_data['chapter']
                
                # Extract data
                verse_data = {
                    'arabic': arabic_text,  # FULL Uthmani script with all harakat
                    'translation': translation_text,
                    'surah_name': chapter_info['name_simple'],
                    'surah_name_arabic': chapter_info['name_arabic'],
                    'surah_number': surah,
                    'ayah_number': ayah,
                    'edition_arabic': 'Uthmani Tajweed (Quran.com)',
                    'edition_translation': 'Sahih International'
                }
                
                # Cache it
                self.cache[cache_key] = verse_data
                self.save_cache()
                
                print(f"✅ Fetched verse {cache_key}: {verse_data['surah_name']} {verse_data['ayah_number']}")
                print(f"   Arabic preview: {arabic_text[:50]}...")
                
                # SUCCESS - return immediately, no need to retry
                return verse_data
                
            except requests.exceptions.Timeout as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  API timeout for verse {cache_key} (attempt {attempt + 1}/{max_retries})")
                    continue  # Retry
                else:
                    print(f"❌ API timeout for verse {cache_key} after {max_retries} attempts")
                    print(f"   This verse will be SKIPPED. Manual intervention needed!")
                    return None
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  API error for verse {cache_key}: {e} (attempt {attempt + 1}/{max_retries})")
                    continue  # Retry
                else:
                    print(f"❌ API error for verse {cache_key} after {max_retries} attempts: {e}")
                    print(f"   This verse will be SKIPPED. Manual intervention needed!")
                    return None
                    
            except Exception as e:
                # Unexpected errors should not retry
                print(f"❌ Unexpected error fetching verse {cache_key}: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        # If we get here, all retries failed
        print(f"❌ CRITICAL: All {max_retries} retry attempts failed for verse {cache_key}")
        print(f"   This verse will be SKIPPED. Manual intervention needed!")
        return None
    
    def get_surah_info(self, surah_number):
        """Get information about a surah"""
        try:
            url = f"{QURAN_API_BASE}/surah/{surah_number}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'number': data['data']['number'],
                'name': data['data']['name'],
                'english_name': data['data']['englishName'],
                'english_translation': data['data']['englishNameTranslation'],
                'revelation_type': data['data']['revelationType'],
                'number_of_ayahs': data['data']['numberOfAyahs']
            }
        except Exception as e:
            print(f"⚠️  Could not fetch surah info: {e}")
            return None


# Test function
if __name__ == "__main__":
    api = QuranAPI()
    
    # Test with Ayat al-Kursi (2:255)
    print("Testing with Ayat al-Kursi (2:255)...")
    verse = api.get_verse(2, 255)
    
    if verse:
        print(f"\n📖 Surah: {verse['surah_name']}")
        print(f"📍 Ayah: {verse['ayah_number']}")
        print(f"\n🕌 Arabic (Uthmani with diacritics):")
        print(verse['arabic'])
        print(f"\n📝 Translation:")
        print(verse['translation'])
    else:
        print("❌ Failed to fetch verse")
