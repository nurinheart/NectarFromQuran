"""
Enhanced Text Renderer - Professional text rendering with styling
Supports: Bold, emphasis, highlighting, proper line breaking
"""

from PIL import Image, ImageDraw
from font_manager import get_font_manager


class TextRenderer:
    """Professional text renderer with styling support"""
    
    def __init__(self, draw, font_manager=None):
        self.draw = draw
        self.fm = font_manager or get_font_manager()
    
    def render_arabic_verse(self, text, x, y, size, color, max_width, line_spacing=2.8, align='right'):
        """
        NEW APPROACH: Render Arabic word-by-word from RIGHT to LEFT
        This preserves the API's perfect letter connections and harakat
        
        No reshaping, no bidi - just position words manually RTL
        """
        from arabic_handler import prepare_arabic_text
        
        # Get font
        font = self.fm.get_arabic_font(size)
        
        # Split into words - API text is already perfect
        words = text.split()
        
        # Measure each word
        word_widths = []
        for word in words:
            bbox = font.getbbox(word)
            word_widths.append(bbox[2] - bbox[0])
        
        # Word spacing
        space_bbox = font.getbbox(' ')
        space_width = (space_bbox[2] - space_bbox[0]) * 2  # Double space
        
        # Wrap words into lines (RTL)
        lines = []  # Each line is a list of word indices
        current_line = []
        current_width = 0
        
        for i, word_width in enumerate(word_widths):
            test_width = current_width + word_width + (space_width if current_line else 0)
            
            if test_width <= max_width:
                current_line.append(i)
                current_width = test_width
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [i]
                current_width = word_width
        
        if current_line:
            lines.append(current_line)
        
        # Calculate line height
        test_bbox = font.getbbox('قُلْ')
        base_height = test_bbox[3] - test_bbox[1]
        line_height = int(base_height * line_spacing)
        
        # Start position
        current_y = y
        
        # Draw each line RTL (right to left)
        for line_word_indices in lines:
            # Calculate total line width
            line_width = sum(word_widths[i] for i in line_word_indices)
            line_width += space_width * (len(line_word_indices) - 1)
            
            # Starting x position (right side)
            if align == 'right':
                line_x = x + max_width
            else:
                line_x = x + (max_width + line_width) // 2
            
            # Draw words from right to left
            for i in reversed(line_word_indices):
                word = words[i]
                word_width = word_widths[i]
                
                # Position from right
                word_x = line_x - word_width
                
                # Draw the word (no manipulation - preserve API perfection!)
                self.draw.text((word_x, current_y), word, fill=color, font=font)
                
                # Move left for next word
                line_x = word_x - space_width
            
            current_y += line_height
        
        return current_y
    
    def render_english_text(self, text, x, y, size, color, max_width, 
                           line_spacing=1.7, bold=False, align='left'):
        """
        Render English text with optional bold
        LEFT-ALIGNED for English (LTR language)
        Returns: final_y position after rendering
        """
        font = self.fm.get_english_font(size, bold=bold)
        
        # Wrap text
        lines = self._wrap_text(text, font, max_width)
        
        # Calculate line height
        line_height = int(font.getbbox('A')[3] * line_spacing)
        current_y = y
        
        # Draw each line - LEFT ALIGNED for English
        for line in lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            
            if align == 'center':
                line_x = x + (max_width - line_width) // 2
            elif align == 'left':
                line_x = x
            else:  # right
                line_x = x + max_width - line_width
            
            self.draw.text((line_x, current_y), line, fill=color, font=font)
            current_y += line_height
        
        return current_y
    
    def render_heading(self, text, x, y, size, color, bold=True, center=True):
        """Render heading (centered or left-aligned)"""
        font = self.fm.get_english_font(size, bold=bold)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        
        if center:
            # Assuming full width is IMAGE_WIDTH (1080)
            centered_x = (1080 - text_width) // 2
        else:
            centered_x = x
        
        self.draw.text((centered_x, y), text, fill=color, font=font)
        return y + int(bbox[3] * 1.5)
    
    def render_reference(self, text, x, y, size, color, center=True):
        """
        Render reference with mixed Arabic/English
        Example: "Az-Zumar (39:53)"
        """
        from arabic_handler import prepare_arabic_text
        
        # Use mixed font (supports both Arabic and English)
        font = self.fm.get_mixed_font(size, bold=False)
        
        # Prepare text (handles mixed content)
        prepared_text = prepare_arabic_text(text)
        
        bbox = font.getbbox(prepared_text)
        text_width = bbox[2] - bbox[0]
        
        if center:
            text_x = (1080 - text_width) // 2
        else:
            text_x = x
        
        self.draw.text((text_x, y), prepared_text, fill=color, font=font)
        return y + int(bbox[3] * 1.5)
    
    def render_attribution(self, text, x, y, size, color):
        """Render attribution (e.g., "— Sahih International")"""
        font = self.fm.get_english_font(size, bold=False)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        
        centered_x = (1080 - text_width) // 2
        self.draw.text((centered_x, y), text, fill=color, font=font)
        return y + int(bbox[3] * 1.5)
    
    def render_watermark(self, text, x, y, size, color, opacity=180):
        """Render watermark with transparency"""
        font = self.fm.get_english_font(size, bold=False)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        
        centered_x = (1080 - text_width) // 2
        
        # Add alpha channel for transparency
        if isinstance(color, str):
            # Convert hex to RGB
            color = color.lstrip('#')
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            color = (r, g, b, opacity)
        elif len(color) == 3:
            color = (*color, opacity)
        
        self.draw.text((centered_x, y), text, fill=color, font=font)
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
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
