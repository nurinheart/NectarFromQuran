"""
Configuration for Quranic Verse Post Generator

🎨 EASY CUSTOMIZATION GUIDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. FONT SIZES (Line ~50-80):
   - arabic_verse: 85 (Arabic text - make it bigger/smaller)
   - heading: 60 (Page titles like "Verse of Reflection")
   - translation: 65 (English translation text)
   - tafsir: 58 (Tafsir explanation text)
   - example: 60 (Real-life example text)
   - reference: 50 (Surah reference at bottom)
   
2. HEADING TEXTS (Line ~85):
   - Change "Verse of Reflection" to your preferred heading
   - Customize all 4 slide headings
   
3. GRAIN EFFECT (Line ~100):
   - grain_intensity: 0.15 (0.0 = no grain, 0.3 = very grainy)
   - grain_noise: 25 (15-40, higher = more visible grain)
   
4. THEME (Line 40):
   - DEFAULT_THEME: Choose from "sage_cream", "elegant_black", "teal_gold"
   
5. WATERMARK (Line ~110):
   - Change "@NectarFromQuran" to your Instagram handle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1350

THEMES = {
    "teal_gold": {
        "name": "Teal & Gold",
        "bg_colors": ["#0F4C5C", "#1A7A8A"],  # Deep teal to bright teal - subtle gradient
        "text_color": "#FFFFFF",  # White for perfect readability
        "arabic_color": "#FFD700",  # Gold for Arabic - elegant contrast
        "heading_color": "#FFD700",  # White for modern minimalist look
        "source_color": "#E8E8E8",  # Softer light gray - less harsh
        "accent_color": "#1A7A8A",
    },
    "sage_cream": {
        "name": "Sage & Cream",
        "bg_colors": ["#E8F3E8", "#D4E7D4"],  # Light sage to soft green - subtle gradient
        "text_color": "#1B3A1B",  # Dark green for excellent contrast
        "arabic_color": "#2E7D32",  # Rich green for Arabic
        "heading_color": "#2E7D32",  # Darker for better hierarchy
        "source_color": "#4CAF50",  # Muted green - more sophisticated
        "accent_color": "#2E7D32",
    },
    "elegant_black": {
        "name": "Elegant Black & Gold",
        "bg_colors": ["#1A1A1A", "#000000"],  # Black to dark gray - subtle gradient
        "text_color": "#FFFFFF",  # Pure white for maximum contrast
        "arabic_color": "#FFD700",  # Gold for Arabic - premium feel
        "heading_color": "#FFD700",  # White for clean modern look
        "source_color": "#A8A8A8",  # Softer gray - more refined
        "accent_color": "#FFD700",
    }
}

DEFAULT_THEME = "sage_cream"

# ===== THEME ROTATION =====
# Set to True to rotate through themes (one theme per post)
# Set to False to use only DEFAULT_THEME
ENABLE_THEME_ROTATION = True
ROTATION_THEMES = ["elegant_black", "sage_cream", "teal_gold"]  # Order of rotation

# ===== HIGHLIGHTING SETTINGS =====
# Control keyword highlighting in translation, tafsir, and example slides
ENABLE_HIGHLIGHTING = True  # Set to False to disable all highlighting
HIGHLIGHT_MAX_WORDS = 4     # Maximum number of words to highlight per slide (3-5 recommended)
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = True  # True = use theme accent color, False = always gold

# ===== QUOTE MARKS SETTINGS =====
# Control quote mark styling for tafsir slides
USE_CURLY_QUOTES = True      # True = use " " (curly/smart quotes), False = use " (straight quotes)
BOLD_QUOTE_MARKS = False     # True = make quotes bold and larger, False = same size as text

# ===== LAYOUT SETTINGS =====
PADDING = 100  # Increased for better breathing room
LINE_SPACING = 1.6  # More generous for readability
MAX_TEXT_WIDTH = IMAGE_WIDTH - (PADDING * 2)
ARABIC_LINE_SPACING = 1.8  # More space for harakat clarity

# ===== FONT SIZES - ADJUST THESE TO YOUR PREFERENCE =====
# Increase/decrease these numbers to change text sizes
CAIRO_FONTS = {
    "arabic_verse": {
        "size": 60,           # 🔤 ARABIC VERSE SIZE - reduced for less cluttered look
        "family": "Amiri", 
        "line_height": 2.0,   # More generous spacing for breathing room
        "max_width": 940      # Increased to reduce excessive right padding
    },
    "heading": {
        "size": 40,           # 📌 HEADING SIZE - slightly larger for hierarchy
        "family": "Montserrat",  # Montserrat for beautiful modern look (was mislabeled as Product Sans)
        "weight": "bold"
    },
    "translation": {
        "size": 45,           # 📝 TRANSLATION - smaller for elegance
        "family": "Montserrat",  # Montserrat for consistency
        "max_width": 850,     # Narrower for better composition
        "line_height": 1.5    # Better line spacing
    },
    "tafsir": {
        "size": 42,           # 📖 TAFSIR - slightly smaller for hierarchy
        "family": "Montserrat",  # Montserrat for consistency
        "max_width": 850,
        "line_height": 1.4
    },
    "example": {
        "size": 42,           # 💡 EXAMPLE - balanced size
        "family": "Montserrat",  # Montserrat for consistency
        "max_width": 850,
        "line_height": 1.4
    },
    "reference": {
        "size": 30,           # 🔖 REFERENCE - smaller, more subtle
        "family": "Montserrat",  # Montserrat for consistency
        "weight": "bold"      # Bold weight same as heading
    },
    "watermark": {
        "size": 25,           # 💧 WATERMARK - smaller, less intrusive
        "family": "Montserrat",  # Montserrat for consistency
        "weight": "normal"    # Regular weight
    }
}

# ===== HEADING TEXT - CUSTOMIZE YOUR HEADINGS =====
HEADING_TEXTS = {
    "arabic_slide": "Verse of Reflection",           # Heading for Slide 1 (Arabic)
    "translation_slide": "English Translation",      # Heading for Slide 2 (Translation)
    "tafsir_slide": "Tazkirul Qur'an",            # Heading for Slide 3 (Tafsir)
    "example_slide": "Reflection"                    # Heading for Slide 4 (Example) - Neutral and non-prescriptive
}

# ===== LAYOUT POSITIONING =====
CAIRO_LAYOUT = {
    "heading_y": 120,                    # Closer to top for modern look
    "reference_y": IMAGE_HEIGHT - 160,   # More space from bottom
    "watermark_y": IMAGE_HEIGHT - 70,    # Better spacing from reference
    "text_padding": 80,                  # More generous padding
    "vertical_center_offset": 50         # Slight offset for visual balance
}

# ===== VISUAL EFFECTS - ADJUST TO YOUR PREFERENCE =====
PATTERN_SETTINGS = {
    'grain_intensity': 0.3,   # 🎨 Grainy texture intensity (0.0 = none, 0.3 = very grainy) - INCREASED
    'grain_noise': 40,         # Grain noise amount (15-40) - INCREASED for more visible grain
    'glass_opacity': 0.85,     # Glassmorphism opacity (0.0-1.0) - not used by default
    'blur_amount': 15          # Blur for glass effect (5-30) - not used by default
}

# Quick access for grain intensity (main control)
GRAIN_INTENSITY = PATTERN_SETTINGS['grain_intensity']

# ===== BRANDING =====
WATERMARK = "@NectarFromQuran"       # Your Instagram handle
WATERMARK_SIZE = 28                   # Watermark size (use CAIRO_FONTS['watermark']['size'] instead)
WATERMARK_OPACITY = 120              # Watermark opacity (0-255)

# ===== POSTING SCHEDULE =====
POSTING_SCHEDULE = {
    "morning_time": "00:00",  # Format: "HH:MM" in 24-hour format
    "night_time": "15:00",    # Format: "HH:MM" in 24-hour format (21:00 = 9 PM)
    "posts_per_day": 2,       # Number of posts per day
    "cleanup_days": 7         # Keep files for 7 days, delete older
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💡 QUICK ADJUSTMENT EXAMPLES:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Want BIGGER text? Increase these:
#   - CAIRO_FONTS["translation"]["size"] = 70  (currently 65)
#   - CAIRO_FONTS["arabic_verse"]["size"] = 95  (currently 85)
#
# Want MORE grain effect?
#   - PATTERN_SETTINGS['grain_intensity'] = 0.25  (currently 0.15)
#   - PATTERN_SETTINGS['grain_noise'] = 35  (currently 25)
#
# Want LESS grain effect?
#   - PATTERN_SETTINGS['grain_intensity'] = 0.08  (currently 0.15)
#   - PATTERN_SETTINGS['grain_noise'] = 18  (currently 25)
#
# Want to change slide headings?
#   - HEADING_TEXTS["arabic_slide"] = "القرآن الكريم"
#   - HEADING_TEXTS["translation_slide"] = "Translation"
#
# Want to use a different theme?
#   - DEFAULT_THEME = "elegant_black"  (currently "sage_cream")
#   - Options: "sage_cream", "elegant_black", "teal_gold"
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
