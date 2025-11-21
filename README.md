# 🕌 NectarFromQuran

**Automated Instagram Posting System** - Daily Quranic Verses with Professional Design

Fully automated system that posts authentic Quranic content to Instagram 2× daily using GitHub Actions.

## 🚀 Production Ready

✅ **Authentic Content**: Fetches verses & Tazkirul Quran tafsir from APIs  
✅ **Perfect Arabic**: Cairo/Pango rendering with harakat (diacritics)  
✅ **Smart Design**: Dynamic 1-10 slides based on content length  
✅ **Fully Automated**: GitHub Actions (no computer needed after setup)  
✅ **Story Sharing**: Auto-shares first slide to story with post link  
✅ **Zero Maintenance**: Self-cleaning, endless verse tracking  

## 📸 Features

### 📖 Content (100% Authentic)
- **Quranic Verses**: Fetched from API (never made up)
- **Translation**: Sahih International (from API)
- **Tafsir**: Tazkirul Quran - naturally concise (700-1500 chars)
- **Full Content**: No summarization, complete authentic explanations
- **Endless Posting**: Tracks posted verses, never repeats
- **Reflection**: AI-generated practical application (only non-API content)

### 🎨 Design
- **Perfect Arabic**: Cairo/Pango rendering engine (no broken harakat)
- **Product Sans Font**: Modern, professional typography
- **3 Premium Themes**: Elegant Black, Sage Cream, Teal Gold
- **Grain Texture**: Subtle analog photography aesthetic
- **Responsive Slides**: 1-10 slides per post (Instagram optimized)
- **Navigation**: Clear "Swipe →" indicators

### 🤖 Automation
- **GitHub Actions**: Runs on cloud (24/7 operation)
- **Scheduled Posts**: 2× daily (morning & night, customizable)
- **Auto Story Share**: Posts + story in one workflow
- **Auto Cleanup**: Deletes images after 7 days
- **No Manual Work**: Set up once, runs forever
- **Session Auth**: Secure Instagram login (60-day sessions)

## 🚀 Quick Start (10 Minutes)

### 1. Verify Production Readiness
```bash
python3 verify_production.py
pip install -r requirements.txt
```

### 2. Get Instagram Session
```bash
python3 get_instagram_session.py
```
Copy the JSON output.

### 3. Configure GitHub Secrets
In GitHub: **Settings → Secrets → Actions → New secret**
- `INSTAGRAM_USERNAME`: Your Instagram username
- `INSTAGRAM_SESSION_DATA`: Paste the JSON from step 2

### 4. Push & Deploy
```bash
git add .
git commit -m "Production ready"
git push
```

### 5. Test & Go Live
- Go to **Actions** tab → **Daily Quran Posts** → **Run workflow**
- Verify post appears on Instagram
- Workflow auto-runs at 06:00 & 21:00 UTC daily

**📖 Full Guide:** See [QUICK_START.md](QUICK_START.md) for detailed instructions.

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **[QUICK_START.md](QUICK_START.md)** | 10-minute deployment guide |
| **[PRODUCTION_SETUP.md](PRODUCTION_SETUP.md)** | Complete setup instructions |
| **[PRE_FLIGHT_CHECKLIST.md](PRE_FLIGHT_CHECKLIST.md)** | Pre-deployment verification |
| **[PRODUCTION_READY.md](PRODUCTION_READY.md)** | System architecture & features |
| **[config.py](config.py)** | All settings with examples |

---

## 📂 Project Structure

```
NectarFromQuran/
├── create_post.py            # Main script (generate → post → story → cleanup)
├── generate_post_cairo.py    # Image generation with Cairo rendering
├── auto_tafsir_fetcher.py    # Fetch Tazkirul Quran from API
├── quran_api.py              # Fetch verses from API
├── cairo_renderer.py         # Perfect Arabic rendering
├── instagram_poster.py       # Instagram API integration
├── config.py                 # Configuration (theme, fonts, schedule)
├── requirements.txt          # Python dependencies
├── session.json              # Instagram session (local only)
├── posted_verses.json        # Tracking posted verses
├── quran_cache.json          # Cached API responses
├── .github/workflows/
│   └── daily-posts.yml       # 5× daily automation
├── fonts/                    # Product Sans fonts
├── samples/                  # Design samples (generated)
└── output/                   # Generated posts
```

## 🎨 Design Samples

After running `python3 generate_post.py`, check:
- `samples/minimalist_*/` - Clean modern style
- `samples/pattern_*/` - Geometric patterns
- `samples/calligraphy_*/` - Artistic calligraphy

Each folder contains 4+ carousel slides showing:
1. Arabic verse (Uthmani script)
2. English translation
3. Tafsir explanation
4. (Additional tafsir slides if needed)

## 🕌 Posting Schedule

5 times daily aligned with prayer times (UTC):
- 04:00 UTC (Fajr time)
- 11:00 UTC (Dhuhr time)
- 14:00 UTC (Asr time)
- 17:00 UTC (Maghrib time)
- 20:00 UTC (Isha time)

## 📖 Themes & Verses

10 themes with 10 verses each = 100 total verses:
1. **Mercy** - Allah's infinite mercy and forgiveness
2. **Patience** - Rewards of patience and perseverance
3. **Gratitude** - Being thankful to Allah
4. **Prayer** - Importance and virtues of Salah
5. **Family** - Rights and responsibilities
6. **Knowledge** - Seeking and applying knowledge
7. **Trust in Allah** - Tawakkul and reliance
8. **Charity** - Giving for Allah's sake
9. **Guidance** - Following the straight path
10. **Hope** - Optimism and hope in Allah

## 🔧 Customization

### Change Theme
Edit `config.py`:
```python
DEFAULT_THEME = "forest_green"  # Any theme name
```

### Change Style
Edit `generate_post.py` line 18:
```python
style="calligraphy"  # minimalist, pattern, or calligraphy
```

### Add More Verses
Edit `quran_data.py` and add to `THEMATIC_VERSES` dict.

### Adjust Posting Times
Edit `.github/workflows/daily-posts.yml` cron schedules.

## 🛠️ Technical Details

### Arabic Text Handling (ROOT FIX)
- Uses `arabic-reshaper` for proper letter connection
- Uses `python-bidi` for RTL text direction
- Uthmani script from AlQuran API
- Full diacritics (تشكيل) preserved
- No rendering errors or boxes

### Carousel Posts
- 4-10 slides per post (Instagram limit)
- Auto-splits long tafsir across multiple slides
- Smart text wrapping for Arabic and English
- Consistent design across all slides

### API & Caching
- AlQuran Cloud API for verses
- Local caching to avoid repeated API calls
- Offline fallback for cached verses
- Timeout handling

## 📱 Testing Locally

Generate a single post:
```python
from generate_post import QuranPostGenerator

generator = QuranPostGenerator("teal_gold", style="minimalist")
slide_paths, index, verse_data = generator.generate_post()

print(f"Generated {len(slide_paths)} slides:")
for path in slide_paths:
    print(f"  - {path}")
```

## 🤲 Sadaqah Jariyah

This project is intended as Sadaqah Jariyah (ongoing charity). Every person who benefits from these verses, reflects on them, or applies their teachings will bring reward to all involved.

May Allah accept this effort and make it a means of guidance for many. Ameen.

## 📄 License

This project is open source and available for anyone to use for spreading the message of the Quran.

---

**Built with ❤️ for the sake of Allah**
