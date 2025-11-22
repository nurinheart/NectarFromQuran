"""
Cairo + Pango renderer for proper Arabic text with harakat
This fixes ALL harakat positioning issues that PIL couldn't handle
"""
import os
import sys
import platform

# Set library paths BEFORE importing cairocffi
if platform.system() == "Darwin":  # macOS
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
    
    # Set environment for dynamic library loading
    os.environ['DYLD_LIBRARY_PATH'] = ":".join(lib_paths) + ":" + os.environ.get('DYLD_LIBRARY_PATH', '')
    os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = ":".join(lib_paths)
    
    # Also set cairocffi to use specific library path
    import cairocffi
    # Manually load the Cairo library from homebrew path
    try:
        cairocffi.cairo = cairocffi.ffi.dlopen('/opt/homebrew/opt/cairo/lib/libcairo.2.dylib')
    except:
        pass  # Fall back to default loading

import cairocffi as cairo
import pangocffi as pango
import pangocairocffi
from PIL import Image
import io


class CairoArabicRenderer:
    """Render Arabic text with perfect harakat positioning using Cairo + Pango"""
    
    def __init__(self, width=1080, height=1350):
        self.width = width
        self.height = height
        self._verify_fonts()
    
    def _verify_fonts(self):
        """Verify Arabic fonts are available via fontconfig (for Cairo/Pango)"""
        import subprocess
        try:
            # Check if fc-list is available
            result = subprocess.run(['fc-list', ':lang=ar'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout:
                print("✅ Arabic fonts found via fontconfig:")
                # Show first 3 fonts
                fonts = [line for line in result.stdout.split('\n') if line][:3]
                for font in fonts:
                    print(f"   {font[:80]}")
            else:
                print("⚠️  No Arabic fonts found via fontconfig - using system fallback")
        except:
            print("⚠️  Could not verify fonts (fc-list not available)")
    
    def render_arabic_verse(self, text, font_family="Amiri", font_size=50, 
                          bg_color=(245, 242, 237), text_color=(80, 60, 40),
                          max_width=900, line_height=1.5, align='right', transparent_bg=False):
        """
        Render Arabic text with proper harakat positioning
        
        Args:
            text: Arabic text with harakat (from Quran API)
            font_family: Font name (Amiri, Scheherazade New, Noto Naskh Arabic)
            font_size: Base font size
            bg_color: Background RGB tuple
            text_color: Text RGB tuple
            max_width: Maximum text width in pixels
            line_height: Line spacing multiplier
            align: 'left', 'center', or 'right'
            transparent_bg: If True, return transparent background
        
        Returns:
            PIL Image with perfectly rendered Arabic text
        """
        # Create Cairo surface
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        context = cairo.Context(surface)
        
        # Fill background or transparent
        if not transparent_bg:
            context.set_source_rgb(bg_color[0]/255, bg_color[1]/255, bg_color[2]/255)
            context.paint()
        
        # Create Pango layout
        layout = pangocairocffi.create_layout(context)
        layout._set_width(pango.units_from_double(max_width))
        
        # Set alignment
        if align == 'right':
            layout._set_alignment(pango.Alignment.RIGHT)
        elif align == 'center':
            layout._set_alignment(pango.Alignment.CENTER)
        else:
            layout._set_alignment(pango.Alignment.LEFT)
        
        layout._set_spacing(pango.units_from_double(font_size * (line_height - 1)))
        
        # Set font with proper OpenType features
        font_desc_str = f"{font_family} {font_size}"
        font_description = pango.pango.pango_font_description_from_string(font_desc_str.encode('utf-8'))
        layout._set_font_description(pango.FontDescription(font_description))
        
        # Set text
        layout._set_text(text)
        
        # Get text dimensions
        text_width, text_height = layout.get_size()
        text_width = pango.units_to_double(text_width)
        text_height = pango.units_to_double(text_height)
        
        # Calculate position
        padding = 100  # Standard padding from edges
        
        # For right-aligned text (Arabic), position the layout box to minimize right padding
        # For left/center aligned, center the box horizontally
        if align == 'right':
            # Push text box to the right with minimal right padding (20px - reduced from 40px)
            x = self.width - max_width - 20
        else:
            # Center the layout box horizontally for left/center alignment
            x = (self.width - max_width) / 2
        
        # Vertically center the text
        y = (self.height - text_height) / 2
        
        # Set text color
        context.set_source_rgb(text_color[0]/255, text_color[1]/255, text_color[2]/255)
        
        # Move to position and render
        context.move_to(x, y)
        pangocairocffi.show_layout(context, layout)
        
        # Convert Cairo surface to PIL Image
        return self._surface_to_pil(surface)
    
    def highlight_random_words(self, text, theme_color="#FFD700", max_words=4):
        """
        Randomly highlight words in text for visual interest
        Highlights up to max_words important words (default 4)
        Returns text with Pango markup for bold and colored highlights
        
        NOTE: Text must NOT contain existing markup - this function adds markup
        """
        import random
        
        # Split into words, preserving punctuation
        words = text.split()
        
        if len(words) == 0:
            return text
        
        # Use fixed maximum number of words, not percentage
        # This ensures consistent highlighting regardless of text length
        num_to_highlight = min(max_words, len(words))
        
        # Select random word indices to highlight
        # Comprehensive list of unworthy words that don't convey meaningful content
        skip_words = {
            # Articles
            'the', 'a', 'an',
            # Conjunctions
            'and', 'or', 'but', 'so', 'yet', 'nor',
            # Prepositions
            'in', 'on', 'at', 'to', 'for', 'of', 'with', 'from', 'by', 'about', 'into', 'through', 
            'over', 'under', 'above', 'below', 'between', 'among', 'during', 'before', 'after',
            # Pronouns
            # Common verbs (forms of be, have, do)
            'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'having',
            'do', 'does', 'did', 'doing', 'done',
            # Modal verbs
            'can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must',
            # Common adverbs
            'very', 'too', 'also', 'just', 'only', 'even', 'still', 'already', 'yet', 'then',
            'here', 'there', 'now', 'when', 'where', 'how', 'why',
            # Other common words
            'if', 'as', 'than', 'such', 'some', 'any', 'all', 'each', 'every', 'both', 'few',
            'more', 'most', 'other', 'another', 'much', 'many', 'own', 'same', 'so', 'no', 'not',
            'i.e.', 'e.g.', 'etc.', 'vs', 'via'
        }
        highlightable_indices = [i for i, word in enumerate(words) 
                                 if len(word.strip('.,!?;:')) >= 4 and word.lower().strip('.,!?;:') not in skip_words]
        
        if len(highlightable_indices) == 0:
            return text
        
        # Random selection - ensure we don't try to highlight more words than available
        # If we have fewer highlightable words, use what we have (min 1, max available)
        num_to_highlight = max(1, min(num_to_highlight, len(highlightable_indices)))
        selected_indices = random.sample(highlightable_indices, num_to_highlight)
        
        # Build highlighted text
        result = []
        for i, word in enumerate(words):
            if i in selected_indices:
                # Strip all punctuation (including brackets, quotes, commas), highlight core word, then re-add punctuation
                import string
                # Extended punctuation list including brackets, quotes, commas
                punct = '.,!?;:\'"()[]{}""''—–-/\\`~@#$%^&*+=<>|'
                stripped = word.strip(punct)
                
                # Find leading and trailing punctuation
                leading_punct = ''
                trailing_punct = ''
                
                # Extract leading punctuation
                for char in word:
                    if char in punct:
                        leading_punct += char
                    else:
                        break
                
                # Extract trailing punctuation
                for char in reversed(word):
                    if char in punct:
                        trailing_punct = char + trailing_punct
                    else:
                        break
                
                # Build result: leading_punct + HIGHLIGHTED_WORD + trailing_punct
                if stripped:  # Only highlight if there's actual word content
                    result.append(f'{leading_punct}<b><span foreground="{theme_color}">{stripped}</span></b>{trailing_punct}')
                else:
                    result.append(word)  # Keep original if only punctuation
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def render_english_text(self, text, font_family="Product Sans", font_size=40,
                          bg_color=(245, 242, 237), text_color=(80, 60, 40),
                          max_width=900, alignment="left", transparent_bg=False, line_height=1.6,
                          highlight_keywords=False, accent_color="#FFD700", 
                          add_opening_quote=False, add_closing_quote=False):
        """
        Render English text (for translations, tafsir, examples)
        
        Args:
            text: English text
            font_family: Font name
            font_size: Font size
            bg_color: Background RGB tuple
            text_color: Text RGB tuple
            max_width: Maximum text width
            alignment: 'left', 'center', or 'right'
            line_height: Line spacing multiplier (default 1.6)
            highlight_keywords: If True, highlight important Islamic keywords
            accent_color: Color for highlights (uses theme accent color)
        
        Returns:
            PIL Image with rendered text
        """
        # Create Cairo surface
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        context = cairo.Context(surface)
        
        # Fill background or transparent
        if not transparent_bg:
            context.set_source_rgb(bg_color[0]/255, bg_color[1]/255, bg_color[2]/255)
            context.paint()
        
        # Create Pango layout
        layout = pangocairocffi.create_layout(context)
        layout._set_width(pango.units_from_double(max_width))
        
        # Set alignment
        if alignment == "center":
            layout._set_alignment(pango.Alignment.CENTER)
        elif alignment == "right":
            layout._set_alignment(pango.Alignment.RIGHT)
        else:
            layout._set_alignment(pango.Alignment.LEFT)
        
        # Set line spacing
        layout._set_spacing(pango.units_from_double(font_size * (line_height - 1)))
        
        # Set font
        font_desc_str = f"{font_family} {font_size}"
        font_description = pango.pango.pango_font_description_from_string(font_desc_str.encode('utf-8'))
        layout._set_font_description(pango.FontDescription(font_description))
        
        # Apply random word highlighting FIRST (before adding quotes)
        # This avoids escaping issues with markup
        if highlight_keywords:
            # Import config to get settings
            from config import ENABLE_HIGHLIGHTING, HIGHLIGHT_MAX_WORDS, USE_ACCENT_COLOR_FOR_HIGHLIGHTS
            
            if ENABLE_HIGHLIGHTING:
                # Use theme accent color or always gold based on config
                highlight_color = accent_color if USE_ACCENT_COLOR_FOR_HIGHLIGHTS else "#FFD700"
                text = self.highlight_random_words(text, theme_color=highlight_color, max_words=HIGHLIGHT_MAX_WORDS)
                # Now text has highlighting markup
        
        # Add stylish bold quotes AFTER highlighting (so quotes aren't highlighted)
        if add_opening_quote:
            # Large bold opening quote
            text = f'<span size="x-large" weight="bold">"</span>{text}'
        if add_closing_quote:
            # Large bold closing quote
            text = f'{text}<span size="x-large" weight="bold">"</span>'
        
        # Check if we have any markup to render
        has_markup = '<span' in text or '<b>' in text or '<i>' in text
        
        # Set the text with markup if present
        if has_markup:
            pango.pango.pango_layout_set_markup(layout._pointer, text.encode('utf-8'), -1)
        else:
            layout._set_text(text)
        
        layout._set_wrap(pango.WrapMode.WORD)
        
        # Get text dimensions for vertical centering
        text_width, text_height = layout.get_size()
        text_width = pango.units_to_double(text_width)
        text_height = pango.units_to_double(text_height)
        
        # Calculate position
        x = (self.width - max_width) / 2  # Center the max_width box
        y = (self.height - text_height) / 2  # Vertically center
        
        # Set text color
        context.set_source_rgb(text_color[0]/255, text_color[1]/255, text_color[2]/255)
        
        # Move to position and render
        context.move_to(x, y)
        pangocairocffi.show_layout(context, layout)
        
        # Convert to PIL Image
        return self._surface_to_pil(surface)
    
    def _surface_to_pil(self, surface):
        """Convert Cairo surface to PIL Image"""
        # Get raw image data
        buf = surface.get_data()
        
        # Create PIL Image from buffer (Cairo uses BGRA format)
        img = Image.frombuffer(
            "RGBA",
            (self.width, self.height),
            buf,
            "raw",
            "BGRA",
            0,
            1
        )
        
        # Return RGBA to preserve transparency for compositing
        return img
    
    def measure_text_height(self, text, font_family="Amiri", font_size=50, max_width=900, line_height=1.5):
        """
        Measure the height that rendered text will occupy
        
        Returns:
            int: Height in pixels
        """
        # Create temporary surface for measurement
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        context = cairo.Context(surface)
        
        # Create Pango layout
        layout = pangocairocffi.create_layout(context)
        layout._set_width(pango.units_from_double(max_width))
        layout._set_spacing(pango.units_from_double(font_size * (line_height - 1)))
        
        # Set font
        font_desc_str = f"{font_family} {font_size}"
        font_description = pango.pango.pango_font_description_from_string(font_desc_str.encode('utf-8'))
        layout._set_font_description(pango.FontDescription(font_description))
        
        # Set text
        layout._set_text(text)
        
        # Get dimensions
        text_width, text_height = layout.get_size()
        text_height = pango.units_to_double(text_height)
        
        return int(text_height)


def test_cairo_renderer():
    """Test the Cairo renderer with real Quranic verse"""
    renderer = CairoArabicRenderer()
    
    # Test verse (39:53) from API
    arabic_text = "۞ قُلْ يَٰعِبَادِىَ ٱلَّذِينَ أَسْرَفُوا۟ عَلَىٰٓ أَنفُسِهِمْ لَا تَقْنَطُوا۟ مِن رَّحْمَةِ ٱللَّهِ ۚ إِنَّ ٱللَّهَ يَغْفِرُ ٱلذُّنُوبَ جَمِيعًا ۚ إِنَّهُۥ هُوَ ٱلْغَفُورُ ٱلرَّحِيمُ ﴿٥٣﴾"
    
    # Render with Amiri font
    img = renderer.render_arabic_verse(
        text=arabic_text,
        font_family="Amiri",
        font_size=48,
        bg_color=(245, 242, 237),  # sage_cream background
        text_color=(80, 60, 40),
        max_width=900,
        line_height=1.8
    )
    
    # Save test output
    img.save("output/test_cairo_arabic.png")
    print("✅ Rendered Arabic with Cairo + Pango")
    print("✅ Saved to: output/test_cairo_arabic.png")
    print("✅ Harakat should now be PERFECTLY positioned!")
    
    # Test English translation
    translation = "Say, 'O My servants who have transgressed against themselves [by sinning], do not despair of the mercy of Allah. Indeed, Allah forgives all sins. Indeed, it is He who is the Forgiving, the Merciful.'"
    
    img_english = renderer.render_english_text(
        text=translation,
        font_family="Sans",  # Will use system sans font
        font_size=36,
        bg_color=(245, 242, 237),
        text_color=(80, 60, 40),
        max_width=900,
        alignment="left"
    )
    
    img_english.save("output/test_cairo_english.png")
    print("✅ Rendered English translation")
    print("✅ Saved to: output/test_cairo_english.png")


if __name__ == "__main__":
    test_cairo_renderer()
