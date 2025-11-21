"""
Enhanced Font Manager - Professional Arabic and English Font Rendering
Uses Amiri/Scheherazade/Noto Naskh for Arabic (perfect harakat)
Uses Product Sans for English (with bold, emphasis)
"""

import os
from PIL import ImageFont

# ========== FONT PATHS ==========

# Arabic fonts (VERIFIED to work perfectly with harakat)
ARABIC_FONTS = {
    'amiri_regular': 'fonts/arabic/amiri/Amiri-1.000/Amiri-Regular.ttf',
    'amiri_bold': 'fonts/arabic/amiri/Amiri-1.000/Amiri-Bold.ttf',
    'amiri_quran': 'fonts/arabic/amiri/Amiri-1.000/AmiriQuran.ttf',  # Special Quran style
    'scheherazade_regular': 'fonts/arabic/scheherazade/ScheherazadeNew-4.000/ScheherazadeNew-Regular.ttf',
    'scheherazade_bold': 'fonts/arabic/scheherazade/ScheherazadeNew-4.000/ScheherazadeNew-Bold.ttf',
    'noto_regular': 'fonts/arabic/noto/NotoNaskhArabic/full/ttf/NotoNaskhArabic-Regular.ttf',
    'noto_bold': 'fonts/arabic/noto/NotoNaskhArabic/full/ttf/NotoNaskhArabic-Bold.ttf',
    'noto_medium': 'fonts/arabic/noto/NotoNaskhArabic/full/ttf/NotoNaskhArabic-Medium.ttf',
}

# English fonts
ENGLISH_FONTS = {
    'product_sans_regular': 'fonts/ProductSans-Regular.ttf',
    'product_sans_bold': 'fonts/ProductSans-Bold.ttf',
}

# Font selection priority
ARABIC_PRIORITY = [
    'amiri_regular',      # ✅ WORKING - Beautiful, proper harakat
    'amiri_quran',        # Special Quran style (needs libraqm)
    'scheherazade_regular',  # Beautiful, clear (needs libraqm)
    'noto_regular',       # Modern, clean (works without libraqm)
]

ARABIC_BOLD_PRIORITY = [
    'amiri_bold',
    'scheherazade_bold',
    'noto_bold',
]


class FontManager:
    """Manages font loading with fallbacks"""
    
    def __init__(self):
        self.font_cache = {}
        self._verify_fonts()
    
    def _verify_fonts(self):
        """Verify which fonts are available"""
        print("\n🔤 Font Manager - Verifying fonts...")
        
        print("\n📖 Arabic Fonts:")
        for name, path in ARABIC_FONTS.items():
            if os.path.exists(path):
                print(f"   ✅ {name:25} → {path}")
            else:
                print(f"   ❌ {name:25} → NOT FOUND")
        
        print("\n🔤 English Fonts:")
        for name, path in ENGLISH_FONTS.items():
            if os.path.exists(path):
                print(f"   ✅ {name:25} → {path}")
            else:
                print(f"   ❌ {name:25} → NOT FOUND")
        print()
    
    def get_arabic_font(self, size, bold=False):
        """
        Get Arabic font with perfect harakat support
        Priority: Amiri Quran > Scheherazade > Noto Naskh
        """
        cache_key = f"arabic_{size}_{bold}"
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        priority = ARABIC_BOLD_PRIORITY if bold else ARABIC_PRIORITY
        
        for font_key in priority:
            path = ARABIC_FONTS.get(font_key)
            if path and os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                    # Test with harakat
                    test_bbox = font.getbbox('قُلْ')
                    if test_bbox[2] > 0:
                        self.font_cache[cache_key] = font
                        return font
                except Exception as e:
                    continue
        
        # Final fallback
        print(f"⚠️  No Arabic font found for size {size}, using default")
        return ImageFont.load_default()
    
    def get_english_font(self, size, bold=False):
        """
        Get English font (Product Sans)
        """
        cache_key = f"english_{size}_{bold}"
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        font_key = 'product_sans_bold' if bold else 'product_sans_regular'
        path = ENGLISH_FONTS.get(font_key)
        
        if path and os.path.exists(path):
            try:
                font = ImageFont.truetype(path, size)
                self.font_cache[cache_key] = font
                return font
            except:
                pass
        
        # Fallback to Arabic fonts (they support English too)
        for font_key in ['noto_medium', 'scheherazade_regular']:
            path = ARABIC_FONTS.get(font_key)
            if path and os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                    self.font_cache[cache_key] = font
                    return font
                except:
                    continue
        
        # System fallback
        system_fonts = [
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
        ]
        
        for sys_font in system_fonts:
            if os.path.exists(sys_font):
                try:
                    font = ImageFont.truetype(sys_font, size)
                    self.font_cache[cache_key] = font
                    return font
                except:
                    continue
        
        return ImageFont.load_default()
    
    def get_mixed_font(self, size, bold=False):
        """
        Get font for mixed Arabic/English text (references)
        Use Arabic fonts as they support both
        """
        cache_key = f"mixed_{size}_{bold}"
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        # Use Noto or Scheherazade for mixed text
        priority = ['noto_bold' if bold else 'noto_medium',
                    'scheherazade_bold' if bold else 'scheherazade_regular',
                    'amiri_bold' if bold else 'amiri_regular']
        
        for font_key in priority:
            path = ARABIC_FONTS.get(font_key)
            if path and os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, size)
                    # Test with mixed text
                    test_bbox = font.getbbox('Az-Zumar (39:53)')
                    if test_bbox[2] > 0:
                        self.font_cache[cache_key] = font
                        return font
                except:
                    continue
        
        return self.get_english_font(size, bold)


# Global instance
_font_manager = None

def get_font_manager():
    """Get singleton font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager
