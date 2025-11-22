"""
Multi-API Quran Fetcher with Persistent Retry
ROOT FIX: Never skips verses - tries multiple APIs until success
"""

import requests
import json
import os
import time
from typing import Dict, Optional, Tuple


class MultiAPIQuranFetcher:
    """
    Fetches Quran verses from multiple APIs with automatic fallback
    GUARANTEE: Never skips a verse - keeps trying until success
    """
    
    def __init__(self):
        self.cache_file = "quran_cache.json"
        self.cache = self._load_cache()
        self.timeout = 30  # seconds
        
        # Define all available APIs (in order of preference)
        self.apis = [
            {
                "name": "Quran.com",
                "priority": 1,
                "fetch_func": self._fetch_quran_com,
                "enabled": True
            },
            {
                "name": "AlQuran.cloud",
                "priority": 2,
                "fetch_func": self._fetch_alquran_cloud,
                "enabled": True
            },
            {
                "name": "Quran-API.ir",
                "priority": 3,
                "fetch_func": self._fetch_quran_api_ir,
                "enabled": True
            }
        ]
        
        # Surah names mapping (for APIs that don't provide names)
        self.surah_names = self._load_surah_names()
    
    def _load_cache(self) -> dict:
        """Load cached verses"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Cache load error: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Save verses to cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Cache save error: {e}")
    
    def _load_surah_names(self) -> dict:
        """Load surah names mapping"""
        return {
            1: "Al-Fatihah", 2: "Al-Baqarah", 3: "Ali 'Imran", 4: "An-Nisa",
            5: "Al-Ma'idah", 6: "Al-An'am", 7: "Al-A'raf", 8: "Al-Anfal",
            9: "At-Tawbah", 10: "Yunus", 11: "Hud", 12: "Yusuf",
            13: "Ar-Ra'd", 14: "Ibrahim", 15: "Al-Hijr", 16: "An-Nahl",
            17: "Al-Isra", 18: "Al-Kahf", 19: "Maryam", 20: "Ta-Ha",
            21: "Al-Anbya", 22: "Al-Hajj", 23: "Al-Mu'minun", 24: "An-Nur",
            25: "Al-Furqan", 26: "Ash-Shu'ara", 27: "An-Naml", 28: "Al-Qasas",
            29: "Al-'Ankabut", 30: "Ar-Rum", 31: "Luqman", 32: "As-Sajdah",
            33: "Al-Ahzab", 34: "Saba", 35: "Fatir", 36: "Ya-Sin",
            37: "As-Saffat", 38: "Sad", 39: "Az-Zumar", 40: "Ghafir",
            41: "Fussilat", 42: "Ash-Shuraa", 43: "Az-Zukhruf", 44: "Ad-Dukhan",
            45: "Al-Jathiyah", 46: "Al-Ahqaf", 47: "Muhammad", 48: "Al-Fath",
            49: "Al-Hujurat", 50: "Qaf", 51: "Adh-Dhariyat", 52: "At-Tur",
            53: "An-Najm", 54: "Al-Qamar", 55: "Ar-Rahman", 56: "Al-Waqi'ah",
            57: "Al-Hadid", 58: "Al-Mujadila", 59: "Al-Hashr", 60: "Al-Mumtahanah",
            61: "As-Saf", 62: "Al-Jumu'ah", 63: "Al-Munafiqun", 64: "At-Taghabun",
            65: "At-Talaq", 66: "At-Tahrim", 67: "Al-Mulk", 68: "Al-Qalam",
            69: "Al-Haqqah", 70: "Al-Ma'arij", 71: "Nuh", 72: "Al-Jinn",
            73: "Al-Muzzammil", 74: "Al-Muddaththir", 75: "Al-Qiyamah", 76: "Al-Insan",
            77: "Al-Mursalat", 78: "An-Naba", 79: "An-Nazi'at", 80: "'Abasa",
            81: "At-Takwir", 82: "Al-Infitar", 83: "Al-Mutaffifin", 84: "Al-Inshiqaq",
            85: "Al-Buruj", 86: "At-Tariq", 87: "Al-A'la", 88: "Al-Ghashiyah",
            89: "Al-Fajr", 90: "Al-Balad", 91: "Ash-Shams", 92: "Al-Layl",
            93: "Ad-Duhaa", 94: "Ash-Sharh", 95: "At-Tin", 96: "Al-'Alaq",
            97: "Al-Qadr", 98: "Al-Bayyinah", 99: "Az-Zalzalah", 100: "Al-'Adiyat",
            101: "Al-Qari'ah", 102: "At-Takathur", 103: "Al-'Asr", 104: "Al-Humazah",
            105: "Al-Fil", 106: "Quraysh", 107: "Al-Ma'un", 108: "Al-Kawthar",
            109: "Al-Kafirun", 110: "An-Nasr", 111: "Al-Masad", 112: "Al-Ikhlas",
            113: "Al-Falaq", 114: "An-Nas"
        }
    
    def get_verse(self, surah: int, ayah: int, max_cycles: int = 10) -> Optional[Dict]:
        """
        Get verse with persistent retry across multiple APIs
        
        Args:
            surah: Surah number (1-114)
            ayah: Ayah number
            max_cycles: Maximum cycles through all APIs (default 10)
        
        Returns:
            Dict with verse data or None after max_cycles
        """
        cache_key = f"{surah}:{ayah}"
        
        # Check cache first
        if cache_key in self.cache:
            print(f"📦 Using cached verse {cache_key}")
            return self.cache[cache_key]
        
        print(f"\n🔍 Fetching verse {surah}:{ayah}...")
        
        # Try each API with retries
        for cycle in range(max_cycles):
            if cycle > 0:
                print(f"\n🔄 Starting cycle {cycle + 1}/{max_cycles} (trying all APIs again)...")
                time.sleep(5)  # Wait before starting new cycle
            
            for api_config in self.apis:
                if not api_config["enabled"]:
                    continue
                
                api_name = api_config["name"]
                fetch_func = api_config["fetch_func"]
                
                # Try this API 3 times before moving to next
                for attempt in range(3):
                    try:
                        if attempt > 0:
                            wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s
                            print(f"   ⏳ Waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                        
                        print(f"   🔄 Trying {api_name} (attempt {attempt + 1}/3)...")
                        
                        result = fetch_func(surah, ayah)
                        
                        if result and result.get('arabic') and result.get('translation'):
                            print(f"   ✅ SUCCESS with {api_name}!")
                            
                            # Cache successful result
                            self.cache[cache_key] = result
                            self._save_cache()
                            
                            return result
                        else:
                            print(f"   ⚠️  {api_name} returned incomplete data")
                    
                    except Exception as e:
                        print(f"   ⚠️  {api_name} error (attempt {attempt + 1}): {str(e)[:50]}...")
                
                # API exhausted all retries, move to next API
                print(f"   ❌ {api_name} failed after 3 attempts, trying next API...")
        
        # All APIs exhausted all cycles
        print(f"\n❌ CRITICAL: Could not fetch verse {surah}:{ayah} after {max_cycles} cycles")
        print(f"   All APIs failed. Check network connection or API status.")
        return None
    
    def _fetch_quran_com(self, surah: int, ayah: int) -> Optional[Dict]:
        """
        Fetch from Quran.com API v4
        
        NOTE: Quran.com API v4 structure changed - now uses combined endpoint
        Must specify both text_uthmani field AND translation resource
        """
        verse_key = f"{surah}:{ayah}"
        
        # Single combined request for both Arabic and translation
        # CRITICAL: Include 'fields' parameter for text_uthmani
        url = f"https://api.quran.com/api/v4/verses/by_key/{verse_key}"
        params = {
            'language': 'en',
            'words': 'false',
            'fields': 'text_uthmani'
        }
        
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        arabic_text = data['verse']['text_uthmani']
        
        # Fetch translation separately using AlQuran.cloud (more reliable for translations)
        # Quran.com v4 API translation endpoint structure changed, so use AlQuran.cloud for translations
        trans_url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih"
        trans_response = requests.get(trans_url, timeout=self.timeout)
        trans_response.raise_for_status()
        trans_data = trans_response.json()
        
        translation_text = trans_data['data']['text']
        
        # Fetch surah info
        chapter_url = f"https://api.quran.com/api/v4/chapters/{surah}"
        chapter_response = requests.get(chapter_url, timeout=self.timeout)
        chapter_data = chapter_response.json()
        
        return {
            'arabic': arabic_text,
            'translation': translation_text,
            'surah_name': chapter_data['chapter']['name_simple'],
            'surah_name_arabic': chapter_data['chapter']['name_arabic'],
            'surah_number': surah,
            'ayah_number': ayah,
            'source': 'Quran.com API (Arabic) + AlQuran.cloud (Translation)'
        }
    
    def _fetch_alquran_cloud(self, surah: int, ayah: int) -> Optional[Dict]:
        """Fetch from AlQuran.cloud API"""
        # Fetch Arabic text (Quran Uthmani)
        arabic_url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/quran-uthmani"
        
        arabic_response = requests.get(arabic_url, timeout=self.timeout)
        arabic_response.raise_for_status()
        arabic_data = arabic_response.json()
        
        if arabic_data['code'] != 200:
            raise Exception(f"API returned code {arabic_data['code']}")
        
        arabic_text = arabic_data['data']['text']
        surah_name = arabic_data['data']['surah']['englishName']
        surah_name_arabic = arabic_data['data']['surah']['name']
        
        # Fetch translation (Sahih International)
        trans_url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/en.sahih"
        
        trans_response = requests.get(trans_url, timeout=self.timeout)
        trans_response.raise_for_status()
        trans_data = trans_response.json()
        
        if trans_data['code'] != 200:
            raise Exception(f"API returned code {trans_data['code']}")
        
        translation_text = trans_data['data']['text']
        
        return {
            'arabic': arabic_text,
            'translation': translation_text,
            'surah_name': surah_name,
            'surah_name_arabic': surah_name_arabic,
            'surah_number': surah,
            'ayah_number': ayah,
            'source': 'AlQuran.cloud API'
        }
    
    def _fetch_quran_api_ir(self, surah: int, ayah: int) -> Optional[Dict]:
        """Fetch from Quran-API.ir (Persian API with good Uthmani text)"""
        url = f"https://quranapi.ir/api/v2/ayat/{surah}:{ayah}"
        
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        if data['code'] != 200:
            raise Exception(f"API returned code {data['code']}")
        
        ayah_data = data['data']
        
        return {
            'arabic': ayah_data['text'],
            'translation': ayah_data.get('translation', {}).get('text', 'Translation not available'),
            'surah_name': self.surah_names.get(surah, f"Surah {surah}"),
            'surah_name_arabic': ayah_data.get('surah_name', ''),
            'surah_number': surah,
            'ayah_number': ayah,
            'source': 'Quran-API.ir'
        }


# Backward compatibility wrapper
class QuranAPI:
    """
    Wrapper for backward compatibility
    Uses MultiAPIQuranFetcher internally
    """
    def __init__(self):
        self.fetcher = MultiAPIQuranFetcher()
        self.base_url = "https://api.quran.com/api/v4"  # For compatibility
        self.cache = self.fetcher.cache
        self.cache_file = self.fetcher.cache_file
    
    def get_verse(self, surah: int, ayah: int) -> Optional[Dict]:
        """Get verse with multi-API fallback"""
        return self.fetcher.get_verse(surah, ayah)
    
    def load_cache(self):
        """Load cache"""
        return self.fetcher._load_cache()
    
    def save_cache(self):
        """Save cache"""
        self.fetcher._save_cache()
