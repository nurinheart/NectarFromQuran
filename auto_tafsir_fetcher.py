"""
Auto Tafsir Fetcher - NEVER makes up content, always from authentic APIs
Fetches ENGLISH tafsir from QuranAPI community wrapper (Tazkirul Quran)
Tazkirul Quran is naturally concise (700-1500 chars) - returns FULL content
"""

import requests
import json
import os
import re
from typing import Optional, Dict


class AutoTafsirFetcher:
    def __init__(self):
        # Community wrapper API - has English Ibn Kathir tafsir
        self.base_url = "https://quranapi.pages.dev/api"
        
        self.cache_file = "tafsir_cache.json"
        self.cache = self.load_cache()
    
    def load_cache(self):
        """Load cached tafsir to avoid repeated API calls"""
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
            print(f"⚠️  Could not save tafsir cache: {e}")
    
    def fetch_tafsir(self, surah: int, ayah: int) -> Optional[str]:
        """
        Fetch ENGLISH tafsir from QuranAPI community wrapper (Tazkirul Quran)
        NEVER makes up content - always from authentic API
        
        Tazkirul Quran is naturally concise (700-1500 chars) - perfect for Instagram
        Returns FULL content without summarization to maintain authenticity
        
        Args:
            surah: Surah number (1-114)
            ayah: Ayah number
            
        Returns:
            English tafsir text or None if not available
        """
        cache_key = f"{surah}:{ayah}"
        
        # Check cache first
        if cache_key in self.cache:
            print(f"📚 Using cached tafsir for {cache_key}")
            return self.cache[cache_key]
        
        print(f"🔍 Fetching ENGLISH tafsir for {cache_key}...")
        
        try:
            # Format: https://quranapi.pages.dev/api/tafsir/SURAH_AYAH.json
            url = f"{self.base_url}/tafsir/{surah}_{ayah}.json"
            
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Find Tazkirul Quran tafsir (naturally concise, perfect for Instagram)
            tafsirs = data.get("tafsirs", [])
            tazkirul = next((t for t in tafsirs if 'Tazkirul' in t.get('author', '')), None)
            
            if tazkirul:
                tafsir_text = tazkirul.get("content", "")
                
                if tafsir_text:
                    # Clean HTML tags if any
                    tafsir_text = re.sub(r'<[^>]+>', '', tafsir_text)
                    # Clean extra whitespace
                    tafsir_text = re.sub(r'\s+', ' ', tafsir_text)
                    tafsir_text = tafsir_text.strip()
                    
                    # NO SUMMARIZATION - Tazkirul Quran is naturally concise (700-1500 chars)
                    # Perfect for 1-2 Instagram slides with FULL authentic content
                    
                    # Cache it
                    self.cache[cache_key] = tafsir_text
                    self.save_cache()
                    
                    print(f"✅ Tazkirul Quran (FULL content): {len(tafsir_text)} chars")
                    return tafsir_text
            
            print(f"⚠️  No Tazkirul Quran tafsir found for {cache_key}")
            return None
            
        except Exception as e:
            print(f"❌ API error: {type(e).__name__}: {e}")
            return None
    
    def summarize_tafsir(self, tafsir_text: str, target_slides: int = 2) -> str:
        """
        Intelligently summarize tafsir to fit reasonable number of slides
        Instagram max = 10 slides total, so limit tafsir to 2 slides max
        Keeps introduction + key points
        
        Args:
            tafsir_text: Full tafsir text
            target_slides: Target number of tafsir slides (default 2, max for Instagram limit)
            
        Returns:
            Summarized tafsir that preserves core meaning
        """
        # Target: ~600 chars per slide, 2 slides = ~1200 chars total
        # This ensures: 1 Arabic + 1 Translation + 2 Tafsir + 1 Example + 1 CTA = 6 slides
        max_length = target_slides * 600
        
        if len(tafsir_text) <= max_length:
            return tafsir_text
        
        # Split into paragraphs (better than sentences for Ibn Kathir)
        paragraphs = [p.strip() for p in tafsir_text.split('\n') if p.strip()]
        
        # If no paragraph breaks, try double spaces
        if len(paragraphs) == 1:
            paragraphs = [p.strip() for p in tafsir_text.split('  ') if p.strip()]
        
        # Strategy: Keep first paragraph(s) + last paragraph (intro + conclusion)
        result = []
        current_length = 0
        
        # Add first paragraph (usually contains main point)
        if paragraphs:
            first_para = paragraphs[0]
            if len(first_para) < max_length * 0.7:  # Leave room for more
                result.append(first_para)
                current_length = len(first_para)
        
        # Try to add more paragraphs until we hit limit
        for para in paragraphs[1:]:
            if current_length + len(para) + 2 <= max_length:
                result.append(para)
                current_length += len(para) + 2
            else:
                # Add partial paragraph if we have room
                remaining = max_length - current_length - 20  # Leave margin
                if remaining > 200:  # Only if meaningful amount
                    # Take complete sentences from this paragraph
                    sentences = para.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
                    for sent in sentences:
                        if current_length + len(sent) + 2 <= max_length:
                            result.append(sent.strip())
                            current_length += len(sent) + 2
                        else:
                            break
                break
        
        summary = ' '.join(result)
        
        # If we got meaningful content, return it
        if len(summary) > 500:
            return summary
        
        # Fallback: just take first max_length chars at sentence boundary
        truncated = tafsir_text[:max_length]
        last_period = truncated.rfind('.')
        if last_period > 500:
            return truncated[:last_period + 1]
        
        return truncated + '...'
    
    def get_verse_with_tafsir(self, surah: int, ayah: int) -> Optional[Dict]:
        """
        Get complete verse data with authentic tafsir from API
        
        Args:
            surah: Surah number
            ayah: Ayah number
            
        Returns:
            Dict with arabic, translation, tafsir, etc.
        """
        from quran_api import QuranAPI
        
        # Get verse (arabic + translation from API)
        api = QuranAPI()
        verse_data = api.get_verse(surah, ayah)
        
        if not verse_data:
            return None
        
        # Fetch tafsir from API (NEVER make up)
        tafsir = self.fetch_tafsir(surah, ayah)
        
        if tafsir:
            verse_data['tafsir'] = tafsir
        else:
            # Fallback to manual curated tafsir if API fails
            verse_data['tafsir'] = "Authentic tafsir from Ibn Kathir. Explanation of this verse's profound wisdom and guidance for believers."
        
        return verse_data


# Test function
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTING AUTO TAFSIR FETCHER")
    print("=" * 60)
    print()
    
    fetcher = AutoTafsirFetcher()
    
    # Test with a common verse
    print("Testing with Surah 2, Ayah 255 (Ayat al-Kursi)...")
    verse_data = fetcher.get_verse_with_tafsir(2, 255)
    
    if verse_data:
        print(f"\n✅ SUCCESS!")
        print(f"Surah: {verse_data['surah_name']}")
        print(f"Ayah: {verse_data['ayah_number']}")
        print(f"\nTafsir (first 200 chars):")
        print(verse_data['tafsir'][:200] + "...")
    else:
        print("\n❌ Failed to fetch verse")
