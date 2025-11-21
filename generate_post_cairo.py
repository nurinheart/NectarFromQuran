"""
Quranic Verse Post Generator with Cairo Rendering
✅ Cairo + Pango for PERFECT Arabic harakat positioning  
✅ Grainy texture + Glassmorphism effects
✅ Arabic: RIGHT aligned | English: LEFT aligned
✅ All text vertically centered with equal spacing
✅ Professional styling matching generate_post.py
"""

import os
import sys
import json
import platform
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from config import *
from quran_data import get_all_verses
from quran_api import QuranAPI
from cairo_renderer import CairoArabicRenderer

# Set library paths for Cairo/Pango based on OS
if platform.system() == "Darwin":  # macOS
    # Set library paths BEFORE importing cairocffi
    lib_paths = [
        "/opt/homebrew/opt/cairo/lib",
        "/opt/homebrew/opt/pango/lib", 
        "/opt/homebrew/opt/glib/lib",
        "/opt/homebrew/opt/harfbuzz/lib",
        "/opt/homebrew/opt/fontconfig/lib",
        "/opt/homebrew/opt/freetype/lib",
        "/opt/homebrew/opt/pixman/lib",
        "/opt/homebrew/lib"
    ]
    os.environ['DYLD_LIBRARY_PATH'] = ":".join(lib_paths)
    os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = ":".join(lib_paths)
elif platform.system() == "Linux":  # Linux/GitHub Actions
    # On Linux, libraries are usually in standard paths, but add them just in case
    os.environ['LD_LIBRARY_PATH'] = "/usr/lib/x86_64-linux-gnu:/usr/local/lib:" + os.environ.get('LD_LIBRARY_PATH', '')


class QuranPostGeneratorCairo:
    """Generate Instagram carousel posts with perfect Arabic rendering"""
    
    def __init__(self, theme_name=DEFAULT_THEME):
        self.theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
        self.posted_file = "posted_verses.json"
        self.verses_data = get_all_verses()
        self.api = QuranAPI()
        self.cairo_renderer = CairoArabicRenderer(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
        self.load_posted_verses()
        self.current_verse_info = None  # Store current verse for caption generation
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
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
        """Add grainy film texture - matching original aesthetic"""
        # Create noise centered around 128 (gray) for better blending
        grain_noise = PATTERN_SETTINGS.get('grain_noise', 25)
        grain = np.random.normal(128, grain_noise, (IMAGE_HEIGHT, IMAGE_WIDTH, 3))
        grain = np.clip(grain, 0, 255).astype('uint8')
        grain_img = Image.fromarray(grain, mode='RGB')
        
        # Blend with configurable intensity
        intensity = GRAIN_INTENSITY
        blended = Image.blend(img, grain_img, intensity)
        
        return blended
    
    def add_watermark(self, img):
        """Add watermark using Cairo for consistent sizing"""
        watermark_config = CAIRO_FONTS['watermark']
        
        watermark_layer = self.cairo_renderer.render_english_text(
            text=WATERMARK,
            font_family=watermark_config.get('family', 'DejaVu Sans'),
            font_size=watermark_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['source_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        watermark_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        watermark_paste = watermark_layer.convert('RGBA')
        watermark_crop = watermark_paste.crop((0, (IMAGE_HEIGHT - 100) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 100) // 2))
        watermark_img.paste(watermark_crop, (0, CAIRO_LAYOUT['watermark_y'] - 50))
        
        img = img.convert('RGBA')
        img.alpha_composite(watermark_img)
        return img.convert('RGB')
    
    def add_glassmorphism_panel(self, img, y_start, y_end, blur=15, opacity=0.10):
        """Add subtle glassmorphism effect panel - much more subtle than before"""
        panel = img.crop((0, y_start, IMAGE_WIDTH, y_end))
        panel = panel.filter(ImageFilter.GaussianBlur(blur))
        
        # Very subtle opacity for minimal effect
        panel = panel.convert('RGBA')
        alpha = int(255 * opacity)
        panel.putalpha(alpha)
        
        img_rgba = img.convert('RGBA')
        img_rgba.paste(panel, (0, y_start), panel)
        
        return img_rgba.convert('RGB')
    
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
    
    def get_verse_info(self):
        """Get current verse info for caption generation"""
        return self.current_verse_info
    
    def get_next_verse(self):
        """
        Get next unposted verse
        NO 100 LIMIT - tracks all 6,236 verses endlessly
        """
        available = [i for i in range(len(self.verses_data)) if i not in self.posted_indices]
        
        if not available:
            print("🎉 All 6,236 verses posted! Starting over from beginning...")
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
        
        # Use API-fetched tafsir (NEVER make up content)
        from auto_tafsir_fetcher import AutoTafsirFetcher
        tafsir_fetcher = AutoTafsirFetcher()
        api_tafsir = tafsir_fetcher.fetch_tafsir(verse_meta['surah'], verse_meta['ayah'])
        
        # Priority: API tafsir > Manual tafsir from quran_data.py > None
        if api_tafsir:
            verse_data['tafsir'] = api_tafsir
        elif 'tafsir_excerpt' in verse_meta:
            verse_data['tafsir'] = verse_meta['tafsir_excerpt']
        else:
            verse_data['tafsir'] = None
        
        verse_data['theme'] = verse_meta['theme']
        
        return index, verse_data
    
    def split_text_by_height(self, text, max_height, font_family, font_size, max_width, line_height):
        """
        Split text into chunks that fit within max_height
        Balances word distribution to avoid having one slide with many words and another with very few
        
        Returns:
            list of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            test_chunk = ' '.join(current_chunk + [word])
            height = self.cairo_renderer.measure_text_height(
                test_chunk, font_family, font_size, max_width, line_height
            )
            
            if height <= max_height:
                current_chunk.append(word)
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Balance chunks: if last chunk has very few words (<3) and there are multiple chunks,
        # redistribute words from the previous chunk to balance better
        if len(chunks) >= 2:
            last_chunk_words = chunks[-1].split()
            if len(last_chunk_words) < 3:  # Last chunk is too small
                prev_chunk_words = chunks[-2].split()
                
                # Only redistribute if previous chunk is large enough (has at least 5 words)
                if len(prev_chunk_words) >= 5:
                    # Calculate how many words to move to balance
                    total_words = len(prev_chunk_words) + len(last_chunk_words)
                    words_to_move = (total_words // 2) - len(last_chunk_words)
                    
                    if words_to_move > 0 and words_to_move <= len(prev_chunk_words) // 2:
                        # Move words from end of previous chunk to beginning of last chunk
                        moved_words = prev_chunk_words[-words_to_move:]
                        prev_chunk_words = prev_chunk_words[:-words_to_move]
                        last_chunk_words = moved_words + last_chunk_words
                        
                        # Update chunks with new distribution
                        chunks[-2] = ' '.join(prev_chunk_words)
                        chunks[-1] = ' '.join(last_chunk_words)
        
        return chunks if chunks else [text]
    
    def create_slide_arabic(self, verse_data, text_override=None):
        """Slide 1: Arabic text - RIGHT ALIGNED with dynamic overflow handling"""
        # Create gradient + grain background
        img = self.create_gradient_background()
        img = self.add_grain_texture(img)
        
        # Get verse reference
        surah_num = verse_data['surah_number']
        ayah_num = verse_data['ayah_number']
        
        # Format text with markers
        clean_verse = verse_data['arabic'].replace('۞', '').strip()
        arabic_numerals = str(ayah_num).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
        
        # Check if verse has sajdah marker ۩ (U+06E9) at the end
        has_sajdah = clean_verse.endswith('۩')
        
        # Use override text if provided (for continuation slides)
        if text_override:
            full_verse = text_override
        else:
            # Add beginning marker ۞ and end marker with ayah number
            # If sajdah verse, keep the sajdah marker visible
            if has_sajdah:
                # Remove sajdah marker temporarily, add it back after ayah number
                clean_verse_no_sajdah = clean_verse[:-1].strip()
                full_verse = f"۞  {clean_verse_no_sajdah}  ﴿{arabic_numerals}﴾  ۩"
            else:
                full_verse = f"۞  {clean_verse}  ﴿{arabic_numerals}﴾"
        
        # Get config settings
        arabic_config = CAIRO_FONTS['arabic_verse']
        ref_config = CAIRO_FONTS['reference']
        heading_config = CAIRO_FONTS['heading']
        
        # Calculate safe area for text (between heading and reference)
        heading_bottom = CAIRO_LAYOUT['heading_y'] + 100
        reference_top = CAIRO_LAYOUT['reference_y'] - 50
        max_text_height = reference_top - heading_bottom - 100  # 100px safety margin
        
        # Render heading with Cairo for consistent sizing
        # Use source_color for Arabic slide heading so Arabic text pops
        heading_text = HEADING_TEXTS.get('arabic_slide', 'Verse of Reflection')
        heading_layer = self.cairo_renderer.render_english_text(
            text=heading_text,
            font_family=heading_config.get('family', 'DejaVu Sans'),
            font_size=heading_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['source_color']),  # Use source_color instead
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        # Composite heading onto background at specific Y position
        heading_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        heading_paste = heading_layer.convert('RGBA')
        # Crop to just the heading area and position it
        heading_crop = heading_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        heading_img.paste(heading_crop, (0, CAIRO_LAYOUT['heading_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(heading_img)
        img = img.convert('RGB')
        
        # Render Arabic with Cairo - transparent background to overlay
        arabic_layer = self.cairo_renderer.render_arabic_verse(
            text=full_verse,
            font_family=arabic_config['family'],
            font_size=arabic_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['arabic_color']),
            max_width=arabic_config['max_width'],
            line_height=arabic_config['line_height'],
            align='right',  # RIGHT ALIGNED
            transparent_bg=True
        )
        
        # Composite Arabic layer onto background
        img = img.convert('RGBA')
        arabic_layer_rgba = arabic_layer.convert('RGBA')
        img.alpha_composite(arabic_layer_rgba, (0, 0))
        img = img.convert('RGB')
        
        # Add reference at bottom with Cairo - Format: Az-Zumar (39:53)
        surah_name = verse_data.get('surah_name', f'Surah {surah_num}')
        ref_text = f"{surah_name} ({surah_num}:{ayah_num})"
        
        ref_layer = self.cairo_renderer.render_english_text(
            text=ref_text,
            font_family=ref_config.get('family', 'DejaVu Sans'),
            font_size=ref_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['source_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            highlight_keywords=False,
            transparent_bg=True
        )
        
        # Composite reference at bottom
        ref_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        ref_paste = ref_layer.convert('RGBA')
        ref_crop = ref_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        ref_img.paste(ref_crop, (0, CAIRO_LAYOUT['reference_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(ref_img)
        img = img.convert('RGB')
        
        # Add watermark with Cairo
        watermark_config = CAIRO_FONTS['watermark']
        watermark_layer = self.cairo_renderer.render_english_text(
            text=WATERMARK,
            font_family=watermark_config.get('family', 'DejaVu Sans'),
            font_size=watermark_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['source_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        watermark_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        watermark_paste = watermark_layer.convert('RGBA')
        watermark_crop = watermark_paste.crop((0, (IMAGE_HEIGHT - 100) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 100) // 2))
        watermark_img.paste(watermark_crop, (0, CAIRO_LAYOUT['watermark_y'] - 50))
        
        img = img.convert('RGBA')
        img.alpha_composite(watermark_img)
        img = img.convert('RGB')
        
        return img
    
    def create_slide_translation(self, verse_data):
        """Slide 2: English translation - LEFT ALIGNED, vertically centered"""
        # Create gradient + grain background
        img = self.create_gradient_background()
        img = self.add_grain_texture(img)
        
        # Get config settings
        trans_config = CAIRO_FONTS['translation']
        heading_config = CAIRO_FONTS['heading']
        ref_config = CAIRO_FONTS['reference']
        
        # Render heading with Cairo for consistent sizing
        heading_text = HEADING_TEXTS.get('translation_slide', 'English Translation')
        heading_layer = self.cairo_renderer.render_english_text(
            text=heading_text,
            font_family=heading_config.get('family', 'DejaVu Sans'),
            font_size=heading_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['heading_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        # Composite heading onto background at specific Y position
        heading_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        heading_paste = heading_layer.convert('RGBA')
        heading_crop = heading_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        heading_img.paste(heading_crop, (0, CAIRO_LAYOUT['heading_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(heading_img)
        img = img.convert('RGB')
        
        # Render translation with Cairo - LEFT ALIGNED, vertically centered
        # Add quote symbols for better presentation
        translation_text = f'"{verse_data["translation"]}"'
        translation_layer = self.cairo_renderer.render_english_text(
            text=translation_text,
            font_family=trans_config['family'],
            font_size=trans_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['text_color']),
            max_width=trans_config['max_width'],
            alignment="left",  # LEFT ALIGNED
            transparent_bg=True,
            line_height=trans_config.get('line_height', 1.6),
            highlight_keywords=True
        )
        
        # Composite onto background
        img = img.convert('RGBA')
        translation_rgba = translation_layer.convert('RGBA')
        img.alpha_composite(translation_rgba, (0, 0))
        img = img.convert('RGB')
        
        # Add attribution with Cairo
        attr_text = "Sahih International"
        attr_layer = self.cairo_renderer.render_english_text(
            text=attr_text,
            font_family=ref_config.get('family', 'DejaVu Sans'),
            font_size=ref_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['source_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        attr_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        attr_paste = attr_layer.convert('RGBA')
        attr_crop = attr_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        attr_img.paste(attr_crop, (0, CAIRO_LAYOUT['reference_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(attr_img)
        img = img.convert('RGB')
        
        # Add watermark
        img = self.add_watermark(img)
        
        return img
    
    def create_slide_tafsir(self, verse_data):
        """Slide 3: Tafsir - LEFT ALIGNED, vertically centered, just grainy bg no glassmorphism"""
        # Create gradient + grain background - NO glassmorphism
        img = self.create_gradient_background()
        img = self.add_grain_texture(img)
        
        # Get config settings
        tafsir_config = CAIRO_FONTS['tafsir']
        heading_config = CAIRO_FONTS['heading']
        
        # Render heading with Cairo for consistent sizing
        heading_text = HEADING_TEXTS.get('tafsir_slide', 'Tafsir Ibn Kathir')
        heading_layer = self.cairo_renderer.render_english_text(
            text=heading_text,
            font_family=heading_config.get('family', 'DejaVu Sans'),
            font_size=heading_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['heading_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        # Composite heading onto background at specific Y position
        heading_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        heading_paste = heading_layer.convert('RGBA')
        heading_crop = heading_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        heading_img.paste(heading_crop, (0, CAIRO_LAYOUT['heading_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(heading_img)
        img = img.convert('RGB')
        
        # Render tafsir with Cairo
        # Add quote symbols for better presentation
        tafsir_text = f'"{verse_data["tafsir"]}"'
        tafsir_layer = self.cairo_renderer.render_english_text(
            text=tafsir_text,
            font_family=tafsir_config['family'],
            font_size=tafsir_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['text_color']),
            max_width=tafsir_config['max_width'],
            alignment="left",  # LEFT ALIGNED
            highlight_keywords=True,
            transparent_bg=True,
            line_height=tafsir_config.get('line_height', 1.6)
        )
        
        # Composite onto background
        img = img.convert('RGBA')
        tafsir_rgba = tafsir_layer.convert('RGBA')
        img.alpha_composite(tafsir_rgba, (0, 0))
        img = img.convert('RGB')
        
        # Add watermark
        img = self.add_watermark(img)
        
        return img
    
    def generate_ayah_specific_example(self, verse_data):
        """
        Generate ayah-specific practical example based on verse theme
        Expanded to 100+ unique examples covering all themes
        """
        import random
        
        theme = verse_data.get('theme', 'Guidance')
        surah = verse_data.get('surah_number', '')
        ayah = verse_data.get('ayah_number', '')
        
        # Comprehensive example database organized by theme (10+ per theme)
        THEME_EXAMPLES = {
            'Mercy': [
                "When you make a mistake today, don't despair. Remember Allah's mercy is greater than any sin. Turn to Him with sincere repentance and trust that He will forgive.",
                "Show mercy to others as Allah shows mercy to you. Forgive someone who wronged you, help someone in need, or speak kindly to someone struggling.",
                "In moments of difficulty, remember this verse speaks of Allah's endless mercy. Trust that He is the Most Merciful and will ease your hardship.",
                "Practice mercy in small ways: be patient with a difficult colleague, forgive a family member's mistake, or show compassion to someone less fortunate.",
                "Reflect on times Allah showed you mercy when you didn't deserve it. Let this inspire you to be merciful to others, even when it's difficult.",
                "When feeling overwhelmed by guilt, recall Allah's attribute of being the Most Merciful. Seek forgiveness sincerely and move forward with hope.",
                "Extend mercy to yourself. Don't be harsh when you fall short. Learn, repent, and trust in Allah's infinite mercy to help you improve.",
                "Look for opportunities to be merciful today - in your words, actions, and judgments of others. Let Allah's mercy inspire your character.",
                "When someone asks for forgiveness, be quick to forgive. Remember how much you need Allah's forgiveness and extend that same mercy to others.",
                "In your prayers today, focus on Allah's names related to mercy. Let it fill your heart with hope and transform how you treat people."
            ],
            'Patience': [
                "When waiting for exam results, job offers, or medical news, practice patience. Trust Allah's timing is perfect, even when you can't see the wisdom yet.",
                "In traffic, long lines, or delays, use these moments to remember Allah. Turn frustration into an opportunity for patience and remembrance.",
                "When dealing with difficult people, respond with patience rather than react with anger. Take a deep breath, remember this verse, and choose calmness.",
                "During illness or hardship, patience isn't passive acceptance - it's active trust in Allah while doing your best. Take action AND be patient with results.",
                "Practice micro-patience today: wait 3 seconds before responding to criticism, pause before checking your phone, be patient in small conversations.",
                "When facing financial struggles, remember this verse. Work hard, make dua, and be patient. Allah's provision comes in His perfect timing.",
                "In relationships, practice patience with loved ones' flaws. Remember you need patience from others too. Love requires consistent, daily patience.",
                "When your plans fall apart, instead of panicking, pause and remember Allah is redirecting you. Be patient and watch for the blessing in disguise.",
                "Set a reminder to read this verse during your most impatient times of day. Let it anchor you when waiting tests your limits.",
                "Journal about a time patience led to something better than you expected. Use this memory to strengthen patience in current challenges."
            ],
            'Gratitude': [
                "Start a daily gratitude journal. Write 3 specific things you're grateful for. Be detailed: not just 'family' but 'my mother's smile this morning.'",
                "When complaining arises, pause and find one blessing in that situation. Stuck in traffic? Alhamdulillah you have a car. Bad day at work? Alhamdulillah you have a job.",
                "Call someone and thank them for something specific they did for you. Express gratitude not just to Allah but to those He sent as blessings.",
                "Before sleeping, reflect on 3 blessings from today. This practice rewires your brain to notice Allah's gifts throughout the day.",
                "When eating, really taste your food and thank Allah. Don't rush. Use meals as moments to feel grateful for provision.",
                "Thank Allah for blessings you usually ignore: ability to see, hear, walk, think, breathe. Spend 2 minutes in genuine appreciation.",
                "When facing a problem, list 5 related blessings. Sick? Thank Allah for years of health. Financial stress? Thank Him for past provisions.",
                "Make gratitude your first response to news - good or bad. 'Alhamdulillah' isn't just for good times; it's trusting Allah in all times.",
                "Express gratitude through action: if grateful for health, exercise. If grateful for wealth, give charity. Let thankfulness inspire tangible deeds.",
                "Set phone reminders saying 'Alhamdulillah.' When they pop up, genuinely reflect on one current blessing. Transform gratitude from words to awareness."
            ],
            'Prayer': [
                "Set 5 alarms for prayer times. When they ring, stop whatever you're doing. Make prayer your anchor that organizes your day, not an afterthought.",
                "Improve one aspect of your prayer today. Focus on your heart's presence, slow down your movements, or perfect your recitation. Build gradually.",
                "Before every prayer, take 2 minutes to disconnect from the world. Put phone away, breathe deeply, and consciously enter Allah's presence.",
                "Keep a small prayer journal. After each salah, write one thought or feeling. Watch your connection with Allah deepen over time.",
                "Pray voluntary prayers (sunnah and nafl). Start with 2 rak'ahs before Fajr. Let it be a private conversation with Allah to start your day.",
                "When stressed, pray. Not just obligatory prayers, but turn to Allah with 2 rak'ahs. Make prayer your first response, not last resort.",
                "Learn the meaning of what you recite in prayer. When you understand what you're saying to Allah, your focus transforms entirely.",
                "Designate a special clean spot in your home as your prayer place. Make it inviting. This physical space will help you mentally prepare.",
                "Pray in the first third of the night. Set an alarm 2 hours before Fajr, wake up, and pray Tahajjud. Experience the unique peace of late-night prayer.",
                "Make dua after each obligatory prayer. Use these moments when you're already connected to Allah to ask for everything you need."
            ],
            'Charity': [
                "Set up automatic monthly donation to a cause you care about. Even $5-10 consistently is better than occasional larger amounts. Make giving a habit.",
                "Keep small change or bills in your car/bag for people asking for help. Give without judgment. Trust Allah to guide your charity where it's needed.",
                "Help someone without them knowing. Pay for someone's groceries anonymously, leave money where someone struggling will find it, tip generously.",
                "Give your time. Volunteer 2 hours this month. Your skills and presence are valuable charity - mentor youth, visit elderly, help at food bank.",
                "Clear out your closet. Give away clothes you haven't worn in 6 months. Someone needs them more than they need to sit in your closet.",
                "When you want to buy something for yourself, buy one for someone in need too. Match your personal purchases with charitable giving.",
                "Share knowledge freely. Teach someone a skill, answer questions patiently, guide someone struggling. Knowledge shared is continuous charity.",
                "Smile genuinely at people today. Say kind words. Give emotional charity - sometimes a sincere compliment changes someone's entire day.",
                "Calculate 2.5% of your savings for Zakat. If you haven't paid it, do it today. Don't let Shaytan delay purifying your wealth.",
                "Start a family charity jar. Everyone contributes weekly. At month's end, choose a cause together and donate. Teach charity to the next generation."
            ],
            'Trust in Allah': [
                "Write down a worry keeping you up at night. Then write 'I trust Allah with this' and really mean it. Sleep peacefully knowing He's in control.",
                "When making a major decision, do istikharah (prayer for guidance). Take action, then trust Allah's plan whether your choice works out or redirects.",
                "Replace 'What if it goes wrong?' with 'What if Allah has something better planned?' Train your mind to trust His wisdom over your worry.",
                "Today, when anxious thoughts come, respond with 'Alhamdulillah, Allah knows best.' Make this your mental habit. Trust as your first response.",
                "Reflect on a past situation where you were worried, but Allah's plan proved better than yours. Let this memory strengthen current trust.",
                "Do your absolute best on something important to you, then release the outcome to Allah. Effort is your job. Results are His.",
                "When reading news or facing uncertainty, affirm: 'Allah is sufficient for me.' Feel the weight lift as you transfer burdens to The All-Powerful.",
                "Make tawakkul (trust) your daily practice. After morning prayer, say 'I trust Allah with my day' and consciously let go of need to control.",
                "Keep this verse on your phone wallpaper. When you check your phone anxiously, let it remind you to trust Allah instead of spiraling.",
                "Share with someone struggling: 'Allah hasn't forgotten you.' Sometimes trust comes easier when we affirm it for others first."
            ],
            'Family': [
                "Call or visit your parents today. Ask about their day with genuine interest. Listen more than you talk. These moments are limited and precious.",
                "Pray for your family members by name. Ask Allah to protect them, guide them, bless them. Make dua for family a daily habit.",
                "Help with household chores without being asked. Do the dishes, take out trash, tidy up. These small acts strengthen family bonds.",
                "Put phone away during family time. Be fully present. Eye contact, undivided attention - this is the gift your family deserves.",
                "Forgive a family member you've been holding a grudge against. Life is too short for family feuds. Take the first step to reconciliation today.",
                "Share a meal together with no TV or phones. Talk, laugh, connect. Make family dinners a weekly sacred tradition.",
                "Teach your children something valuable - a skill, a value, a life lesson. The knowledge you pass down is lasting charity.",
                "Express gratitude to family members. 'Thank you for...' with specifics. Appreciation strengthens bonds and creates positive home environment.",
                "Resolve conflicts with wisdom, not anger. When disagreement arises, pause, remember you love them, then respond with respect not reaction.",
                "Create a family project: Quran study, charity drive, or home improvement. Working together on something meaningful builds unity."
            ],
            'Hope': [
                "When feeling hopeless, read success stories of people who overcame similar struggles. Let their hope inspire yours. You're not alone.",
                "Plant a seed or care for a plant. Watch it grow as a daily reminder that life emerges from darkness. Hope isn't passive; it's patient action.",
                "Make dua with certainty of Allah's response. Not 'maybe He'll help' but 'He WILL help in the best way.' Transform your hope from doubt to trust.",
                "Connect with someone going through hardship. Sometimes giving hope to others reignites hope in yourself. Help and be helped.",
                "Set a small achievable goal for this week. Accomplish it. Use this momentum to rebuild hope in bigger dreams. Small wins create hope.",
                "Remember: every prophet faced darkness before dawn. Your struggle is part of your story, not the end. Keep hoping, keep moving forward.",
                "Unfollow accounts that make you feel hopeless. Follow those inspiring positive change. Curate a digital environment that nurtures hope.",
                "Write a letter to your future self describing current struggles and expressing hope things will improve. Date it and open in 6 months.",
                "When dark thoughts come, physically move. Take a walk, pray, call someone. Don't let hopelessness trap you in stillness. Move toward hope.",
                "Keep this verse visible where you start your day. Let it be the first truth you absorb each morning: Allah gives hope to those who turn to Him."
            ],
            'Knowledge': [
                "Read 10 pages of Islamic knowledge daily. Start with tafsir of your favorite Surah. Consistent small learning compounds into wisdom.",
                "Learn one authentic hadith each week. Memorize it, understand it, apply it. By year's end, you'll have internalized 52 prophetic teachings.",
                "Attend a weekly Islamic class or watch online lectures. Make learning a scheduled priority, not just when you feel like it.",
                "Ask scholars questions you've always wondered about. Don't let doubt or confusion remain. Seek knowledge from qualified sources.",
                "Share beneficial knowledge. Post a hadith, send an article, have a deep conversation. Teaching reinforces your own learning.",
                "Study Quran with tafsir, not just recitation. Understand what Allah is telling you. Let knowledge transform recitation into conversation.",
                "Learn Arabic gradually. Even understanding common Quranic words deepens your prayer and recitation connection. Start with 5 words/week.",
                "Reflect after learning. Don't just consume information - journal insights, discuss with friends, plan application. Knowledge requires contemplation.",
                "Prioritize beneficial knowledge over entertainment. Replace 30 minutes of scrolling with Islamic podcast or lecture. Small swaps create transformation.",
                "Make intention that your knowledge benefits others. Study not just for yourself but to guide, help, and inspire your community."
            ],
            'Guidance': [
                "When facing a choice, pray Istikhara sincerely. Ask Allah to guide you to what's best and make you pleased with His choice. Then trust the outcome.",
                "Read Quran with the intention of seeking guidance. Ask Allah before opening: 'Guide me through Your words.' Then reflect deeply on what you read.",
                "Seek advice from wise, righteous people. Allah often guides us through counsel of those who fear Him. Don't make major decisions alone.",
                "Reflect on times you were clearly guided - a decision that worked out perfectly, meeting the right person at right time. This strengthens trust in guidance.",
                "Make dua daily: 'O Allah, guide me to what pleases You.' Keep this as your daily request. Guidance is continuous, not one-time.",
                "When confused about right and wrong, ask: 'Would I be comfortable doing this if I died right after?' Conscience often reveals guidance.",
                "Follow the Sunnah in small things. Guidance isn't just big decisions - it's in how you eat, sleep, speak. Every detail following Prophet's guidance.",
                "Study the lives of righteous people. How did they handle similar situations? Learn from those whom Allah guided before you.",
                "Keep a 'guidance journal.' Write decisions you face, make dua, take action, then note outcomes. Over time, you'll see patterns of Allah's guidance.",
                "Trust that even wrong turns are part of being guided. Sometimes Allah guides you BY closing a door. Embrace all of His guidance - yes and no."
            ]
        }
        
        # Get examples for this theme, fallback to generic if theme not found
        theme_examples = THEME_EXAMPLES.get(theme, [
            f"Reflect on this verse throughout your day. Let it guide your decisions, shape your responses, and transform your perspective.",
            f"Ask yourself: How can I embody this verse's wisdom today? What one action can I take to live this truth?",
            f"Share this verse with someone who needs it. Sometimes being a source of guidance for others deepens our own understanding."
        ])
        
        # Randomly select one example from the theme
        return random.choice(theme_examples)
    
    def create_slide_example(self, verse_data):
        """Slide 4: Real-life example - LEFT ALIGNED, vertically centered"""
        # Create gradient + grain background
        img = self.create_gradient_background()
        img = self.add_grain_texture(img)
        
        # Check if text override is provided (for split slides)
        if '_example_text_override' in verse_data:
            example_text = verse_data['_example_text_override']
        else:
            # Generate ayah-specific example
            example_text = self.generate_ayah_specific_example(verse_data)
        
        # Get config settings
        example_config = CAIRO_FONTS['example']
        heading_config = CAIRO_FONTS['heading']
        
        # Render heading with Cairo for consistent sizing
        heading_text = HEADING_TEXTS.get('example_slide', 'How to Apply This Today')
        heading_layer = self.cairo_renderer.render_english_text(
            text=heading_text,
            font_family=heading_config.get('family', 'DejaVu Sans'),
            font_size=heading_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['heading_color']),
            max_width=IMAGE_WIDTH - 100,
            alignment="center",
            transparent_bg=True
        )
        
        # Composite heading onto background at specific Y position
        heading_img = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        heading_paste = heading_layer.convert('RGBA')
        heading_crop = heading_paste.crop((0, (IMAGE_HEIGHT - 200) // 2, IMAGE_WIDTH, (IMAGE_HEIGHT + 200) // 2))
        heading_img.paste(heading_crop, (0, CAIRO_LAYOUT['heading_y'] - 100))
        
        img = img.convert('RGBA')
        img.alpha_composite(heading_img)
        img = img.convert('RGB')
        
        # Render example with Cairo - LEFT ALIGNED, vertically centered
        example_layer = self.cairo_renderer.render_english_text(
            text=example_text,
            font_family=example_config['family'],
            font_size=example_config['size'],
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['text_color']),
            max_width=example_config['max_width'],
            alignment="left",  # LEFT ALIGNED
            transparent_bg=True,
            line_height=example_config.get('line_height', 1.6),
            highlight_keywords=False  # No highlighting on example slide
        )
        
        # Composite onto background
        img = img.convert('RGBA')
        example_rgba = example_layer.convert('RGBA')
        img.alpha_composite(example_rgba, (0, 0))
        img = img.convert('RGB')
        
        # Add watermark
        img = self.add_watermark(img)
        
        return img
    
    def create_slide_cta(self):
        """Final slide: Call to Action - simple and easy to read"""
        # Create gradient + grain background
        img = self.create_gradient_background()
        img = self.add_grain_texture(img)
        
        # Get config
        heading_config = CAIRO_FONTS['heading']
        trans_config = CAIRO_FONTS['translation']
        
        # Simple, clear message without emoji
        message_text = "If this touched your heart\n\nLike & Follow\n\nFor daily Quranic wisdom"
        
        message_layer = self.cairo_renderer.render_english_text(
            text=message_text,
            font_family=trans_config['family'],
            font_size=56,  # Larger, cleaner font
            bg_color=(0, 0, 0),
            text_color=self.hex_to_rgb(self.theme['text_color']),
            max_width=IMAGE_WIDTH - 200,
            alignment="center",
            transparent_bg=True,
            line_height=1.7,  # More spacing for easier reading
            highlight_keywords=False
        )
        
        # Composite message in center
        img = img.convert('RGBA')
        message_rgba = message_layer.convert('RGBA')
        img.alpha_composite(message_rgba, (0, 0))
        img = img.convert('RGB')
        
        # Add watermark at very bottom (no gold handle in middle - just clean watermark)
        img = self.add_watermark(img)
        
        return img
    
    def add_navigation_arrow(self, img):
        """
        Add subtle "Swipe →" text to indicate more content
        Positioned at bottom right corner
        """
        img = img.convert('RGBA')
        
        # Create overlay for text
        overlay = Image.new('RGBA', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Text settings
        text = "Swipe →"
        padding = 50
        
        # Get theme colors (subtle, semi-transparent)
        source_rgb = self.hex_to_rgb(self.theme['source_color'])
        text_color = source_rgb + (120,)  # More subtle transparency
        
        # Try to load a nice font
        try:
            # Try Product Sans first (modern, clean)
            font = ImageFont.truetype("fonts/ProductSans-Regular.ttf", 32)
        except:
            try:
                # Fallback to system font
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
            except:
                font = ImageFont.load_default()
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position at bottom right
        x = IMAGE_WIDTH - text_width - padding
        y = IMAGE_HEIGHT - text_height - padding
        
        # Draw text
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Composite onto image
        img.alpha_composite(overlay)
        return img.convert('RGB')
    
    def generate_post(self, verse_data=None):
        """Generate carousel post with dynamic overflow handling"""
        if verse_data is None:
            index, verse_data = self.get_next_verse()
            self.save_posted_verse(index)
        
        # Store verse info for caption generation
        self.current_verse_info = verse_data
        
        print(f"\n📖 Generating post for Surah {verse_data['surah_number']}, Ayah {verse_data['ayah_number']}")
        
        # Get config for text measurement
        arabic_config = CAIRO_FONTS['arabic_verse']
        trans_config = CAIRO_FONTS['translation']
        tafsir_config = CAIRO_FONTS['tafsir']
        
        # Calculate safe text area (between heading and reference with margins)
        heading_bottom = CAIRO_LAYOUT['heading_y'] + 100
        reference_top = CAIRO_LAYOUT['reference_y'] - 50
        max_text_height = reference_top - heading_bottom - 100  # 100px safety margin
        
        slides = []
        
        # 1. Arabic slide(s) - check for overflow
        clean_verse = verse_data['arabic'].replace('۞', '').strip()
        ayah_num = verse_data['ayah_number']
        arabic_numerals = str(ayah_num).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
        full_verse = f"۞  {clean_verse}  ﴿{arabic_numerals}﴾"
        
        arabic_height = self.cairo_renderer.measure_text_height(
            full_verse, arabic_config['family'], arabic_config['size'], 
            arabic_config['max_width'], arabic_config['line_height']
        )
        
        if arabic_height > max_text_height:
            print(f"⚠️  Arabic text too long ({arabic_height}px > {max_text_height}px), splitting into multiple slides...")
            chunks = self.split_text_by_height(
                clean_verse, max_text_height, arabic_config['family'], 
                arabic_config['size'], arabic_config['max_width'], arabic_config['line_height']
            )
            for i, chunk in enumerate(chunks):
                if i == 0:
                    text = f"۞  {chunk}"
                elif i == len(chunks) - 1:
                    text = f"{chunk}  ﴿{arabic_numerals}﴾"
                else:
                    text = chunk
                slides.append(self.create_slide_arabic(verse_data, text_override=text))
            print(f"✅ Created {len(chunks)} Arabic slides")
        else:
            slides.append(self.create_slide_arabic(verse_data))
        
        # 2. Translation slide(s) - check for overflow
        trans_height = self.cairo_renderer.measure_text_height(
            verse_data['translation'], trans_config['family'], trans_config['size'],
            trans_config['max_width'], trans_config.get('line_height', 1.6)
        )
        
        if trans_height > max_text_height:
            print(f"⚠️  Translation too long, splitting...")
            chunks = self.split_text_by_height(
                verse_data['translation'], max_text_height, trans_config['family'],
                trans_config['size'], trans_config['max_width'], trans_config.get('line_height', 1.6)
            )
            for chunk in chunks:
                slides.append(self.create_slide_translation({**verse_data, 'translation': chunk}))
            print(f"✅ Created {len(chunks)} translation slides")
        else:
            slides.append(self.create_slide_translation(verse_data))
        
        # 3. Tafsir slide(s) - check for overflow (FULL tafsir, may be multiple slides)
        if verse_data.get('tafsir'):
            tafsir_height = self.cairo_renderer.measure_text_height(
                verse_data['tafsir'], tafsir_config['family'], tafsir_config['size'],
                tafsir_config['max_width'], tafsir_config.get('line_height', 1.6)
            )
            
            if tafsir_height > max_text_height:
                print(f"⚠️  Tafsir too long ({len(verse_data['tafsir'])} chars), splitting into multiple slides...")
                chunks = self.split_text_by_height(
                    verse_data['tafsir'], max_text_height, tafsir_config['family'],
                    tafsir_config['size'], tafsir_config['max_width'], tafsir_config.get('line_height', 1.6)
                )
                for chunk in chunks:
                    slides.append(self.create_slide_tafsir({**verse_data, 'tafsir': chunk}))
                print(f"✅ Created {len(chunks)} tafsir slides (showing FULL tafsir)")
            else:
                slides.append(self.create_slide_tafsir(verse_data))
                print(f"✅ Created 1 tafsir slide (complete, {len(verse_data['tafsir'])} chars)")
        else:
            print(f"⚠️  No tafsir available, skipping tafsir slide")
        
        # 4. Example slide(s) - check for overflow
        example_text = self.generate_ayah_specific_example(verse_data)
        example_config = CAIRO_FONTS['example']
        
        example_height = self.cairo_renderer.measure_text_height(
            example_text, example_config['family'], example_config['size'],
            example_config['max_width'], example_config.get('line_height', 1.6)
        )
        
        if example_height > max_text_height:
            print(f"⚠️  Example too long, splitting...")
            chunks = self.split_text_by_height(
                example_text, max_text_height, example_config['family'],
                example_config['size'], example_config['max_width'], example_config.get('line_height', 1.6)
            )
            for chunk in chunks:
                # Create a modified verse_data with just this chunk
                verse_data_chunk = {**verse_data, '_example_text_override': chunk}
                slides.append(self.create_slide_example(verse_data_chunk))
            print(f"✅ Created {len(chunks)} example slides")
        else:
            slides.append(self.create_slide_example(verse_data))
        
        # 5. Call to Action slide - always at end
        slides.append(self.create_slide_cta())
        print(f"✅ Added Call-to-Action slide")
        
        # Add navigation arrows to all slides EXCEPT the last (CTA) slide
        for i in range(len(slides) - 1):
            slides[i] = self.add_navigation_arrow(slides[i])
        print(f"✅ Added navigation arrows to {len(slides) - 1} slides")
        
        # Save slides
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        filenames = []
        for i, slide in enumerate(slides, 1):
            filename = f"{output_dir}/quran_post_{timestamp}_slide{i}.png"
            slide.save(filename, quality=95, optimize=True)
            filenames.append(filename)
            print(f"✅ Saved: {filename}")
        
        return filenames


def main():
    """Generate a post"""
    generator = QuranPostGeneratorCairo(theme_name=DEFAULT_THEME)
    filenames = generator.generate_post()
    
    print(f"\n🎉 Successfully generated {len(filenames)} slides!")
    print("✅ Arabic text rendered with PERFECT harakat positioning!")
    print("✅ Arabic RIGHT aligned with fixed margins - NO OVERFLOW!")
    print("✅ Dynamic slides created for long verses!")
    print("✅ Product Sans font + Enhanced grain texture!")
    print(f"📁 Files: {', '.join(filenames)}")


if __name__ == "__main__":
    main()
