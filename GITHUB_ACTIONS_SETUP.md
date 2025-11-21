# GitHub Actions Setup for Quran Post Generator

## Overview
This workflow automatically generates beautiful Quranic verse posts daily using Cairo + Pango for perfect Arabic harakat rendering.

## Setup Instructions

### 1. Enable GitHub Actions
- Go to your repository settings
- Navigate to **Actions** → **General**
- Enable workflows for your repository

### 2. Configure Secrets (Optional - for Instagram posting)
If you want to automatically post to Instagram:
- Go to **Settings** → **Secrets and variables** → **Actions**
- Add the following secrets:
  - `INSTAGRAM_USERNAME`: Your Instagram username
  - `INSTAGRAM_PASSWORD`: Your Instagram password or app-specific password

### 3. Workflow Schedule
The workflow runs automatically:
- **Daily at 9 AM UTC** (adjust the cron schedule in `.github/workflows/generate_post.yml`)
- **Manual trigger**: Go to Actions tab → Select workflow → Click "Run workflow"

### 4. Fonts in GitHub Actions
The workflow automatically installs:
- ✅ **Amiri** - Primary Arabic font
- ✅ **Noto Naskh Arabic** - Fallback Arabic font
- ✅ Cairo and Pango libraries

On Ubuntu/Linux (GitHub Actions), these fonts are installed via:
```bash
sudo apt-get install fonts-noto-naskh-arabic fonts-amiri
```

### 5. Library Paths
The code automatically detects the OS and sets correct library paths:
- **macOS**: Uses Homebrew paths (`/opt/homebrew/opt/...`)
- **Linux**: Uses system paths (`/usr/lib/x86_64-linux-gnu/...`)

## Manual Local Testing

### macOS (Homebrew):
```bash
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/cairo/lib:/opt/homebrew/opt/pango/lib:/opt/homebrew/opt/glib/lib:/opt/homebrew/lib"
python3 generate_post_cairo.py
```

### Linux/Ubuntu:
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y libcairo2-dev libpango1.0-dev libglib2.0-dev \
    fonts-noto-naskh-arabic fonts-amiri pkg-config

# Install Python packages
pip3 install -r requirements.txt

# Run generator
python3 generate_post_cairo.py
```

## Viewing Generated Images

### In GitHub Actions:
1. Go to **Actions** tab
2. Click on the completed workflow run
3. Scroll down to **Artifacts**
4. Download **quran-post-images.zip**

### Locally:
Generated images are saved in `output/` directory:
- `quran_post_YYYYMMDD_HHMMSS_slide1.png` - Arabic verse
- `quran_post_YYYYMMDD_HHMMSS_slide2.png` - Translation
- `quran_post_YYYYMMDD_HHMMSS_slide3.png` - Tafsir/Explanation
- `quran_post_YYYYMMDD_HHMMSS_slide4.png` - Real-life Application

## Customization

### Change Schedule
Edit `.github/workflows/generate_post.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9 AM UTC
  # Change to: '0 */6 * * *' for every 6 hours
  # Or: '0 12 * * 1,3,5' for Mon/Wed/Fri at noon
```

### Change Theme
Edit `generate_post_cairo.py`:
```python
generator = QuranPostGeneratorCairo(theme_name="sage_cream")
# Options: "sage_cream", "elegant_black", "teal_gold"
```

## Troubleshooting

### Fonts not found in GitHub Actions
The workflow installs `fonts-amiri` and `fonts-noto-naskh-arabic`. On Linux, Pango automatically finds fonts in:
- `/usr/share/fonts/`
- `/usr/local/share/fonts/`
- `~/.fonts/`

Cairo renderer uses font family names:
- `"Amiri"` → finds system Amiri font
- `"Noto Naskh Arabic"` → finds Noto font
- `"Sans"` → uses system default sans-serif

### Cairo/Pango not found
Ensure these system packages are installed:
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev pkg-config
```

Then install Python bindings:
```bash
pip3 install cairocffi pangocffi pangocairocffi
```

### Images look different on Linux vs macOS
This is normal - different systems have different font rendering engines. The important thing is that **harakat render correctly** on both platforms (they will!).

## Why Cairo + Pango?

Previous attempts using PIL/Pillow failed because:
- ❌ PIL cannot position harakat without libraqm
- ❌ Building Pillow with libraqm is complex and fails often
- ❌ `arabic-reshaper` breaks harakat positioning
- ❌ `python-bidi` breaks letter connections

Cairo + Pango solution:
- ✅ Native OpenType support (proper mark positioning)
- ✅ Built-in text shaping
- ✅ Works reliably on Linux and macOS
- ✅ Used by professional Quran apps
- ✅ Perfect harakat rendering every time

## Success Criteria
✅ Arabic harakat don't overlap
✅ Letters connect properly (الله as one word, not separate)
✅ Verse markers (۞) display correctly
✅ All 4 slides generate successfully
✅ Works in GitHub Actions
