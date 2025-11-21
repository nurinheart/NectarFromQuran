"""
Quranic Verse Post Generator - PROFESSIONAL EDITION
✅ Arabic: Amiri Quran / Scheherazade / Noto Naskh (perfect harakat)
✅ English: Product Sans (bold styling, proper formatting)
✅ No boxes anywhere - professional fonts for all text
✅ Proper RTL rendering (top-to-bottom)
✅ Grainy bg + Glassmorphism
✅ Enhanced text styling and emphasis
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import json
import os
from datetime import datetime
import random
import numpy as np
from config import *
from quran_data import get_all_verses
from quran_api import QuranAPI
from arabic_handler import prepare_arabic_text
from font_manager import get_font_manager
from text_renderer import TextRenderer


class QuranPostGenerator:
    def __init__(self, theme_name=DEFAULT_THEME, style="pattern"):
        """Initialize with professional fonts and rendering"""
        self.theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.style = style
        self.posted_file = "posted_verses.json"
        self.verses_data = get_all_verses()
        self.api = QuranAPI()
        self.font_manager = get_font_manager()
        self.load_posted_verses()
    
    def load_posted_verses(self):
        """Load posted verse indices"""
        if os.path.exists(self.posted_file):
            with open(self.posted_file, 'r') as f:
                self.posted_indices = json.load(f)
        else:
            self.posted_indices = []
    
    def save_posted_verse(self, index):
        """Save posted verse index"""
        self.posted_indices.append(index)
        with open(self.posted_file, 'w') as f:
            json.dump(self.posted_indices, f)
    
    def get_next_verse(self):
        """Get next unposted verse"""
        available = [i for i in range(len(self.verses_data)) if i not in self.posted_indices]
        
        if not available:
            print("🔄 All verses posted! Resetting...")
            self.posted_indices = []
            available = list(range(len(self.verses_data)))
        
        index = available[0]
        verse_meta = self.verses_data[index]
        
        # Fetch from API with FULL harakat
        verse_data = self.api.get_verse(verse_meta['surah'], verse_meta['ayah'])
        
        if not verse_data:
            print(f"⚠️  Skipping verse...")
            self.posted_indices.append(index)
            return self.get_next_verse()
        
        verse_data['theme'] = verse_meta['theme']
        verse_data['tafsir'] = verse_meta['tafsir_excerpt']
        
        return index, verse_data
    
    def get_font(self, font_type, size=None):
        """
        Get font with Arabic support - ROOT FIX for boxes and harakat
        STRATEGY: Different fonts for different text types for best rendering
        """
        if size is None:
            size = FONTS[font_type]['size']
        
        # STRATEGY 1: Arabic text (verses) - MUST support harakat perfectly
        if 'arabic' in font_type:
            # Priority order based on testing
            arabic_priority = [
                '/Library/Fonts/Arial Unicode.ttf',  # Best harakat display
                '/System/Library/Fonts/Supplemental/DecoTypeNaskh.ttc',  # Beautiful Naskh
                '/System/Library/Fonts/Supplemental/KufiStandardGK.ttc',  # Good alternative
            ]
            
            for font_path in arabic_priority:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, size)
                        # Test with Arabic + harakat
                        test_bbox = font.getbbox('قُلْ')
                        if test_bbox[2] > 0:
                            return font
                    except:
                        continue
            
            # Fallback to any available Arabic font
            for font_path in ARABIC_FONTS:
                try:
                    font = ImageFont.truetype(font_path, size)
                    if font.getbbox('ا')[2] > 0:
                        return font
                except:
                    continue
            
            print(f"⚠️  No Arabic font found, using default")
            return ImageFont.load_default()
        
        # STRATEGY 2: References and headings with mixed Arabic/English
        # Use fonts that support BOTH without boxes
        if font_type in ['source', 'heading']:
            mixed_text_fonts = [
                '/Library/Fonts/Arial Unicode.ttf',  # Universal support
                '/System/Library/Fonts/Supplemental/DecoTypeNaskh.ttc',
                '/System/Library/Fonts/Supplemental/KufiStandardGK.ttc',
            ]
            
            for font_path in mixed_text_fonts:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, size)
                        # Test with mixed text
                        test_bbox = font.getbbox('Az-Zumar (39:53)')
                        if test_bbox[2] > 0:
                            return font
                    except:
                        continue
        
        # STRATEGY 3: Pure English text (translation, tafsir)
        # Try Product Sans first for aesthetics, fallback to Arial Unicode
        if font_type in ['translation', 'tafsir']:
            # Try Product Sans
            if os.path.exists(FONT_PATHS.get('product_sans_bold', '')):
                try:
                    return ImageFont.truetype(FONT_PATHS['product_sans_bold'], size)
                except:
                    pass
            
            # Fallback to Arial Unicode (always works)
            if os.path.exists('/Library/Fonts/Arial Unicode.ttf'):
                try:
                    return ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', size)
                except:
                    pass
        
        # FINAL FALLBACK: Universal fonts that support everything
        universal_fallbacks = [
            '/Library/Fonts/Arial Unicode.ttf',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        ]
        
        for font_path in universal_fallbacks:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
        
        return ImageFont.load_default()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient_background(self):
        """Create gradient background"""
        img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))
        draw = ImageDraw.Draw(img)
        
        color1 = self.hex_to_rgb(self.theme['bg_colors'][0])
        color2 = self.hex_to_rgb(self.theme['bg_colors'][1])
        
        for y in range(IMAGE_HEIGHT):
            factor = y / IMAGE_HEIGHT
            r = int(color1[0] * (1 - factor) + color2[0] * factor)
            g = int(color1[1] * (1 - factor) + color2[1] * factor)
            b = int(color1[2] * (1 - factor) + color2[2] * factor)
            draw.line([(0, y), (IMAGE_WIDTH, y)], fill=(r, g, b))
        
        return img
    
    def add_grain_texture(self, img):
        """Add grainy film texture - ROOT FIX for aesthetic grainy background"""
        # Create grain layer
        grain = np.random.normal(0, 25, (IMAGE_HEIGHT, IMAGE_WIDTH, 3))
        grain_img = Image.fromarray(grain.astype('uint8'), mode='RGB')
        
        # Blend with original
        intensity = PATTERN_SETTINGS['grain_intensity']
        blended = Image.blend(img, grain_img, intensity)
        
        return blended
    
    def add_glassmorphism_panel(self, img, y_start, y_end, blur=15, opacity=0.85):
        """Add glassmorphism effect panel - ROOT FIX for modern aesthetic"""
        # Create panel area
        panel = img.crop((0, y_start, IMAGE_WIDTH, y_end))
        
        # Apply blur for glass effect
        panel = panel.filter(ImageFilter.GaussianBlur(blur))
        
        # Adjust opacity
        panel = panel.convert('RGBA')
        alpha = int(255 * opacity)
        panel.putalpha(alpha)
        
        # Paste back
        img_rgba = img.convert('RGBA')
        img_rgba.paste(panel, (0, y_start), panel)
        
        return img_rgba.convert('RGB')
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def wrap_arabic_text(self, text, font, max_width):
        """Wrap Arabic RTL text - ROOT FIX: Maintain proper top-to-bottom order"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # ROOT FIX: Lines are already in correct visual order after prepare_arabic_text
        # No need to reverse - the bidi algorithm handles RTL correctly
        return lines
    
    def create_slide_arabic(self, verse_data):
        """Slide 1: Arabic verse with perfect harakat - RIGHT ALIGNED"""
        img = self.create_gradient_background()
        
        # Add grain texture for aesthetic
        if self.style == "pattern":
            img = self.add_grain_texture(img)
        
        draw = ImageDraw.Draw(img)
        renderer = TextRenderer(draw, self.font_manager)
        
        # Add heading at top
        renderer.render_heading(
            "Verse of Reflection",
            x=PADDING,
            y=60,
            size=38,
            color=self.theme['heading_color'],
            center=True
        )
        
        # Remove any existing markers from the verse (API might include ۞)
        clean_verse = verse_data['arabic'].replace('۞', '').strip()
        
        # Choose font size based on verse length
        verse_length = len(clean_verse)
        if verse_length < 100:
            arabic_size = 80
        elif verse_length < 200:
            arabic_size = 70
        elif verse_length < 350:
            arabic_size = 58
        else:
            arabic_size = 50  # Very long verses
        
        # Create proper verse markers
        verse_start_marker = "۞"  # Start marker
        ayah_num = verse_data['ayah_number']
        # Convert to Arabic-Indic numerals
        arabic_numerals = str(ayah_num).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
        verse_end_marker = f"﴿{arabic_numerals}﴾"  # ﴿ ﴾ are decorative brackets
        
        # Combine: start marker + verse + end marker
        full_verse = f"{verse_start_marker}  {clean_verse}  {verse_end_marker}"
        
        # Calculate proper vertical position to avoid overlapping with reference
        # Reserve space at bottom for reference (130px) and watermark (60px) = 200px
        # Reserve space at top for heading + margin = 200px
        # Available height = 1350 - 200 - 200 = 950px
        
        available_height = IMAGE_HEIGHT - 400  # Top margin + bottom reserved
        
        # Estimate text height
        num_words = len(full_verse.split())
        line_height = int(arabic_size * ARABIC_LINE_SPACING)
        estimated_lines = (num_words // 4) + 1  # Rough estimate
        estimated_height = estimated_lines * line_height
        
        # Center in available space
        start_y = 200 + (available_height - estimated_height) // 2
        start_y = max(200, min(start_y, 450))  # Clamp between 200-450
        
        renderer.render_arabic_verse(
            full_verse,
            x=PADDING + 50,  # Add left margin for proper right-alignment balance
            y=start_y,
            size=arabic_size,
            color=self.theme['arabic_color'],
            max_width=MAX_TEXT_WIDTH - 100,
            line_spacing=ARABIC_LINE_SPACING,
            align='right'  # RIGHT ALIGNED for Arabic (RTL)
        )
        
        # Reference at bottom (mixed Arabic/English)
        ref_text = f"{verse_data['surah_name']} ({verse_data['surah_number']}:{verse_data['ayah_number']})"
        renderer.render_reference(
            ref_text,
            x=PADDING,
            y=IMAGE_HEIGHT - 130,
            size=42,
            color=self.theme['source_color'],
            center=True
        )
        
        # Watermark
        if WATERMARK:
            renderer.render_watermark(
                WATERMARK,
                x=PADDING,
                y=IMAGE_HEIGHT - 60,
                size=WATERMARK_SIZE,
                color=self.theme['source_color'],
                opacity=WATERMARK_OPACITY
            )
        
        return img
    
    def create_slide_translation(self, verse_data):
        """Slide 2: English translation - LEFT ALIGNED with equal spacing"""
        img = self.create_gradient_background()
        
        if self.style == "pattern":
            img = self.add_grain_texture(img)
        
        draw = ImageDraw.Draw(img)
        renderer = TextRenderer(draw, self.font_manager)
        
        # Calculate vertical centering
        # Reserve 200px at top for heading, 200px at bottom for attribution/watermark
        available_height = IMAGE_HEIGHT - 400
        
        # Estimate text height for centering
        font = self.font_manager.get_english_font(52, bold=False)
        lines = renderer._wrap_text(verse_data['translation'], font, MAX_TEXT_WIDTH - 80)
        line_height = int(font.getbbox('A')[3] * LINE_SPACING)
        text_height = len(lines) * line_height
        
        # Center vertically with equal spacing
        heading_y = 150
        text_start_y = heading_y + 100 + (available_height - text_height) // 2
        
        # Heading (centered)
        renderer.render_heading(
            "English Translation",
            x=PADDING,
            y=heading_y,
            size=46,
            color=self.theme['heading_color'],
            bold=True,
            center=True
        )
        
        # Translation text (LEFT ALIGNED)
        y_pos = renderer.render_english_text(
            verse_data['translation'],
            x=PADDING + 40,
            y=text_start_y,
            size=52,
            color=self.theme['text_color'],
            max_width=MAX_TEXT_WIDTH - 80,
            line_spacing=LINE_SPACING,
            bold=False,
            align='left'  # LEFT ALIGNED
        )
        
        # Source attribution
        renderer.render_attribution(
            "— Sahih International",
            x=PADDING,
            y=IMAGE_HEIGHT - 130,
            size=38,
            color=self.theme['source_color']
        )
        
        # Watermark
        if WATERMARK:
            renderer.render_watermark(
                WATERMARK,
                x=PADDING,
                y=IMAGE_HEIGHT - 60,
                size=WATERMARK_SIZE,
                color=self.theme['source_color'],
                opacity=WATERMARK_OPACITY
            )
        
        return img
    
    def create_slide_tafsir(self, verse_data, part=1):
        """Slide 3: Tafsir - LEFT ALIGNED with equal spacing"""
        img = self.create_gradient_background()
        
        # Apply grain texture AFTER glassmorphism for consistent grainy background
        if self.style == "pattern":
            img = self.add_glassmorphism_panel(
                img, 
                100, 
                IMAGE_HEIGHT - 100,
                blur=PATTERN_SETTINGS['blur_amount'],
                opacity=PATTERN_SETTINGS['glass_opacity']
            )
            img = self.add_grain_texture(img)
        
        draw = ImageDraw.Draw(img)
        renderer = TextRenderer(draw, self.font_manager)
        
        # Calculate vertical centering
        available_height = IMAGE_HEIGHT - 400
        
        # Estimate text height for centering
        font = self.font_manager.get_english_font(46, bold=False)
        lines = renderer._wrap_text(verse_data['tafsir'], font, MAX_TEXT_WIDTH - 120)
        line_height = int(font.getbbox('A')[3] * LINE_SPACING)
        text_height = len(lines) * line_height
        
        # Center vertically with equal spacing
        heading_y = 150
        text_start_y = heading_y + 100 + (available_height - text_height) // 2
        
        # Heading (centered)
        renderer.render_heading(
            "Tafsir Ibn Kathir",
            x=PADDING,
            y=heading_y,
            size=46,
            color=self.theme['heading_color'],
            bold=True,
            center=True
        )
        
        # Tafsir text (LEFT ALIGNED)
        y_pos = renderer.render_english_text(
            verse_data['tafsir'],
            x=PADDING + 40,
            y=text_start_y,
            size=46,
            color=self.theme['text_color'],
            max_width=MAX_TEXT_WIDTH - 80,
            line_spacing=LINE_SPACING,
            bold=False,
            align='left'  # LEFT ALIGNED
        )
        
        # Watermark
        if WATERMARK:
            renderer.render_watermark(
                WATERMARK,
                x=PADDING,
                y=IMAGE_HEIGHT - 60,
                size=WATERMARK_SIZE,
                color=self.theme['source_color'],
                opacity=WATERMARK_OPACITY
            )
        
        return img
    
    def create_slide_real_life_example(self, verse_data):
        """Slide 4: Real-life example - LEFT ALIGNED with equal spacing"""
        img = self.create_gradient_background()
        
        if self.style == "pattern":
            img = self.add_grain_texture(img)
        
        draw = ImageDraw.Draw(img)
        renderer = TextRenderer(draw, self.font_manager)
        
        # Generate contextual real-life example based on the verse theme
        example_text = self._generate_real_life_example(verse_data)
        
        # Calculate vertical centering
        available_height = IMAGE_HEIGHT - 400
        
        # Estimate text height for centering
        font = self.font_manager.get_english_font(48, bold=False)
        lines = renderer._wrap_text(example_text, font, MAX_TEXT_WIDTH - 80)
        line_height = int(font.getbbox('A')[3] * LINE_SPACING)
        text_height = len(lines) * line_height
        
        # Center vertically with equal spacing
        heading_y = 150
        text_start_y = heading_y + 100 + (available_height - text_height) // 2
        
        # Heading (centered)
        renderer.render_heading(
            "How to Apply This Today",
            x=PADDING,
            y=heading_y,
            size=46,
            color=self.theme['heading_color'],
            bold=True,
            center=True
        )
        
        # Example text (LEFT ALIGNED)
        y_pos = renderer.render_english_text(
            example_text,
            x=PADDING + 40,
            y=text_start_y,
            size=48,
            color=self.theme['text_color'],
            max_width=MAX_TEXT_WIDTH - 80,
            line_spacing=LINE_SPACING,
            bold=False,
            align='left'
        )
        
        # Watermark
        if WATERMARK:
            renderer.render_watermark(
                WATERMARK,
                x=PADDING,
                y=IMAGE_HEIGHT - 60,
                size=WATERMARK_SIZE,
                color=self.theme['source_color'],
                opacity=WATERMARK_OPACITY
            )
        
        return img
    
    def _generate_real_life_example(self, verse_data):
        """Generate a contextual real-life example based on verse theme"""
        theme = verse_data.get('theme', '').lower()
        
        # Theme-based examples
        examples = {
            'mercy': "When you make a mistake, remember Allah's endless mercy. Instead of despairing, turn to Him with sincere repentance. Whether it's a harsh word to a loved one or a missed prayer, acknowledge it and seek forgiveness - His door is always open.",
            
            'patience': "During difficult times - waiting for exam results, dealing with health issues, or facing financial struggles - practice patience by remembering Allah's wisdom. Trust that every hardship has a hidden blessing and timing is in His perfect plan.",
            
            'gratitude': "Start each day by listing three blessings: your health, family, or even the ability to breathe. When challenges arise, pause and recall past difficulties Allah helped you through. This practice transforms your perspective and strengthens faith.",
            
            'prayer': "Set reminders for the five daily prayers on your phone. When the call comes, stop whatever you're doing - even if it's work or entertainment. These five pauses ground you, reconnect you with your purpose, and bring peace to your entire day.",
            
            'charity': "Practice regular giving, even if small. Set aside $5 weekly for those in need. It could be food for a homeless person, supporting an orphan, or helping a struggling student. This habit purifies your wealth and softens your heart.",
            
            'forgiveness': "When someone hurts you, take a moment before reacting. Remember times you needed forgiveness. Choose to let go of grudges - not because they deserve it, but because your peace of mind is more valuable than holding onto anger.",
            
            'default': "Reflect on this verse throughout your day. When facing decisions, ask: 'What would this verse teach me to do?' Let its wisdom guide your actions with family, colleagues, and strangers. Small consistent changes create lasting transformation."
        }
        
        # Try to match theme to examples, otherwise use default
        for key in examples:
            if key in theme:
                return examples[key]
        
        return examples['default']
    
    def generate_carousel(self, output_path="output", specific_index=None):
        """Generate full carousel post (4 slides: Arabic, Translation, Tafsir, Real-life Example)"""
        os.makedirs(output_path, exist_ok=True)
        
        # Get verse
        if specific_index is not None:
            index = specific_index
            verse_meta = self.verses_data[index]
            verse_data = self.api.get_verse(verse_meta['surah'], verse_meta['ayah'])
            verse_data['theme'] = verse_meta['theme']
            verse_data['tafsir'] = verse_meta['tafsir_excerpt']
        else:
            index, verse_data = self.get_next_verse()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slides = []
        
        # Slide 1: Arabic
        print(f"📄 Generating Slide 1: Arabic verse...")
        slide1 = self.create_slide_arabic(verse_data)
        path1 = f"{output_path}/verse_{index}_slide1_{timestamp}.png"
        slide1.save(path1, quality=95)
        slides.append(path1)
        
        # Slide 2: Translation
        print(f"📄 Generating Slide 2: Translation...")
        slide2 = self.create_slide_translation(verse_data)
        path2 = f"{output_path}/verse_{index}_slide2_{timestamp}.png"
        slide2.save(path2, quality=95)
        slides.append(path2)
        
        # Slide 3: Tafsir
        print(f"📄 Generating Slide 3: Tafsir...")
        slide3 = self.create_slide_tafsir(verse_data)
        path3 = f"{output_path}/verse_{index}_slide3_{timestamp}.png"
        slide3.save(path3, quality=95)
        slides.append(path3)
        
        # Slide 4: Real-life Example
        print(f"📄 Generating Slide 4: Real-life Example...")
        slide4 = self.create_slide_real_life_example(verse_data)
        path4 = f"{output_path}/verse_{index}_slide4_{timestamp}.png"
        slide4.save(path4, quality=95)
        slides.append(path4)
        
        # Save verse
        if specific_index is None:
            self.save_posted_verse(index)
        
        print(f"✅ Generated carousel: {len(slides)} slides")
        print(f"📖 Verse: {verse_data['surah_name']} {verse_data['ayah_number']}")
        print(f"🎨 Theme: {self.theme['name']} | Style: {self.style}")
        print(f"📝 Arabic preview: {verse_data['arabic'][:30]}...")
        
        return slides, index, verse_data
    
    def generate_post(self, output_path="output", specific_index=None):
        """Alias for generate_carousel - for backward compatibility"""
        return self.generate_carousel(output_path, specific_index)


def generate_all_theme_samples():
    """Generate samples for all 3 themes"""
    print("🎨 Generating samples for all themes...\n")
    
    themes = ["sage_cream", "elegant_black", "teal_gold"]
    
    for theme in themes:
        print(f"\n{'='*60}")
        print(f"Theme: {theme.upper()}")
        print(f"{'='*60}\n")
        
        generator = QuranPostGenerator(theme_name=theme, style="pattern")
        slides, index, verse = generator.generate_carousel("samples", specific_index=0)
        
        print(f"✅ {len(slides)} slides generated for {theme}\n")
    
    print(f"\n{'='*60}")
    print("✅ ALL SAMPLES GENERATED!")
    print(f"{'='*60}")
    print(f"📂 Check 'samples/' folder")
    print(f"🎯 Choose your favorite theme!")


if __name__ == "__main__":
    # Generate samples
    generate_all_theme_samples()
