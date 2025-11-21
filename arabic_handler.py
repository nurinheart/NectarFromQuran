"""
Arabic Text Handler - ROOT FIX for proper RTL and diacritics
Handles Arabic reshaping, bidi, and proper rendering
CRITICAL: Must preserve diacritics and render RTL correctly
"""

from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display

# CRITICAL FIX: Configure reshaper to PRESERVE harakat (diacritics)
# Default reshape() function DELETES harakat!
ARABIC_RESHAPER_CONFIG = {
    'delete_harakat': False,  # MUST be False to keep diacritics
    'support_ligatures': True,
    'shift_harakat_position': False,  # Keep harakat in original position
    'use_unshaped_instead_of_isolated': False,
}

# Create configured reshaper instance
reshaper = ArabicReshaper(configuration=ARABIC_RESHAPER_CONFIG)


def prepare_arabic_text(text):
    """
    NEW APPROACH: Don't manipulate text at all!
    Render word-by-word from right to left
    
    The API provides perfect Uthmani text with proper letter connections
    and harakat positioning. We just need to render it RTL without breaking it.
    
    Returns: Original text (word-level rendering handled in text_renderer)
    """
    # Return text as-is from API
    # The text_renderer will handle word-by-word RTL positioning
    return text


def is_arabic(text):
    """Check if text contains Arabic characters"""
    arabic_ranges = [
        (0x0600, 0x06FF),  # Arabic
        (0x0750, 0x077F),  # Arabic Supplement
        (0x08A0, 0x08FF),  # Arabic Extended-A
        (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
    ]
    
    for char in text:
        code = ord(char)
        for start, end in arabic_ranges:
            if start <= code <= end:
                return True
    return False


def split_arabic_text_by_length(text, max_chars=200):
    """
    Split long Arabic text into chunks for multiple slides
    Tries to split at sentence boundaries
    """
    if len(text) <= max_chars:
        return [text]
    
    # Try to split at periods, question marks, or exclamation marks
    sentences = []
    current = ""
    
    for char in text:
        current += char
        if char in '.!؟۔' and len(current) >= 50:  # Arabic and English punctuation
            sentences.append(current.strip())
            current = ""
    
    if current:
        sentences.append(current.strip())
    
    # Group sentences into chunks under max_chars
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence if current_chunk else sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks if chunks else [text]
