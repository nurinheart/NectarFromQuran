# New Config Options - Quick Reference

## 🎨 Highlighting Controls

### Enable/Disable All Highlighting
```python
ENABLE_HIGHLIGHTING = True  # Set to False to disable all highlighting
```

### Control Highlight Amount
```python
HIGHLIGHT_RATIO = 0.15  # 15% of words highlighted
# Try: 0.10 (10% - less) or 0.20 (20% - more)
```

### Highlight Color
```python
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = True  # Use theme's accent color
# False = always use gold (#FFD700)
```

**How it works**:
- `elegant_black`: Highlights in gold (#FFD700)
- `sage_cream`: Highlights in green (#2E7D32)
- `teal_gold`: Highlights in gold (#FFD700)

---

## 🔄 Theme Rotation

### Enable Theme Rotation
```python
ENABLE_THEME_ROTATION = False  # Set to True to rotate themes
```

### Configure Rotation Order
```python
ROTATION_THEMES = ["elegant_black", "sage_cream", "teal_gold"]
```

**How it works**:
- Post #1: elegant_black
- Post #2: sage_cream
- Post #3: teal_gold
- Post #4: elegant_black (cycles back)
- And so on...

---

## ✅ Fixed: Arabic Spacing

All themes now have **consistent Arabic text spacing**:
- **Right padding**: 40px (fixed)
- **max_width**: 940px (fixed)
- No more spacing differences!

**Before**: elegant_black had less spacing, sage_cream had more  
**After**: All themes identical spacing ✅

---

## 🔧 Examples

### Example 1: No Highlighting
```python
ENABLE_HIGHLIGHTING = False
```

### Example 2: More Highlights with Theme Colors
```python
ENABLE_HIGHLIGHTING = True
HIGHLIGHT_RATIO = 0.25  # 25% highlighted
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = True
```

### Example 3: Subtle Gold Highlights
```python
ENABLE_HIGHLIGHTING = True
HIGHLIGHT_RATIO = 0.10  # Only 10%
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = False  # Always gold
```

### Example 4: Theme Rotation Enabled
```python
ENABLE_THEME_ROTATION = True
DEFAULT_THEME = "elegant_black"  # Ignored when rotation enabled
ROTATION_THEMES = ["elegant_black", "sage_cream"]  # Rotates between 2
```

---

## 📊 Theme Accent Colors Reference

| Theme | Accent Color | RGB | Highlight Effect |
|-------|--------------|-----|------------------|
| elegant_black | Gold (#FFD700) | (255, 215, 0) | Warm, premium |
| sage_cream | Green (#2E7D32) | (46, 125, 50) | Natural, peaceful |
| teal_gold | Gold (#FFD700) | (255, 215, 0) | Vibrant, elegant |

---

## 🎯 Recommended Settings

### For Consistent Branding (Current Setup)
```python
DEFAULT_THEME = "elegant_black"
ENABLE_THEME_ROTATION = False
ENABLE_HIGHLIGHTING = True
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = True
HIGHLIGHT_RATIO = 0.15
```

### For Visual Variety
```python
ENABLE_THEME_ROTATION = True
ROTATION_THEMES = ["elegant_black", "sage_cream", "teal_gold"]
ENABLE_HIGHLIGHTING = True
USE_ACCENT_COLOR_FOR_HIGHLIGHTS = True
HIGHLIGHT_RATIO = 0.15
```

### For Minimal/Clean Look
```python
DEFAULT_THEME = "elegant_black"
ENABLE_THEME_ROTATION = False
ENABLE_HIGHLIGHTING = False  # No highlights at all
```

---

## ⚠️ Important Notes

1. **Theme rotation**: Reads `posted_verses.json` to determine which theme to use
2. **Highlighting**: Only applies to Translation, Tafsir slides (not Arabic, Example, CTA)
3. **Arabic spacing**: Now fixed at 40px right padding across all themes
4. **Config changes**: Take effect on next post (no restart needed)

---

## 🐛 Troubleshooting

**Q: Highlighting not working?**  
A: Check `ENABLE_HIGHLIGHTING = True` in config.py

**Q: Theme not rotating?**  
A: Check `ENABLE_THEME_ROTATION = True` and verify ROTATION_THEMES list

**Q: Want same highlight color across all themes?**  
A: Set `USE_ACCENT_COLOR_FOR_HIGHLIGHTS = False`

**Q: Arabic text spacing different between themes?**  
A: Should be fixed now! All themes use 40px right padding. If still different, check cairo_renderer.py line 127.
