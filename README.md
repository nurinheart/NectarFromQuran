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
├── Core Scripts
│   ├── create_post.py            # Main entry point (generate → post → story → cleanup)
│   ├── generate_post_cairo.py    # Image generation with Cairo/Pango rendering
│   ├── auto_tafsir_fetcher.py    # Fetch Tazkirul Quran tafsir from API
│   ├── quran_api.py              # Fetch verses & translations from API
│   ├── cairo_renderer.py         # Perfect Arabic text rendering
│   ├── instagram_poster.py       # Instagram API integration
│   └── font_manager.py           # Font loading and management
│
├── Configuration
│   ├── config.py                 # All settings (theme, fonts, schedule)
│   └── requirements.txt          # Python dependencies
│
├── Helper Tools
│   ├── get_instagram_session.py # Generate Instagram session for GitHub
│   └── verify_production.py     # Pre-deployment verification
│
├── Documentation
│   ├── README.md                 # This file
│   ├── QUICK_START.md            # 10-minute deployment guide
│   ├── PRODUCTION_SETUP.md       # Complete setup instructions
│   ├── PRE_FLIGHT_CHECKLIST.md  # Pre-deployment checklist
│   ├── PRODUCTION_READY.md       # System architecture & features
│   └── DEPLOYMENT_CHECKLIST.txt  # Quick reference checklist
│
├── Data & Cache
│   ├── posted_verses.json        # Tracks posted verses (git tracked)
│   ├── quran_cache.json          # Cached API responses (git tracked)
│   └── tafsir_cache.json         # Cached tafsir (git tracked)
│
├── GitHub Actions
│   └── .github/workflows/
│       └── daily-posts.yml       # Automated posting (2× daily)
│
├── Assets
│   ├── fonts/                    # Arabic fonts (Amiri, Noto, Scheherazade)
│   └── output/                   # Generated images (temporary)
│
└── .gitignore                    # Git exclusions
```

## 🔧 Customization

### Change Theme
Edit `config.py`:
```python
DEFAULT_THEME = "elegant_black"  # Options: elegant_black, sage_cream, teal_gold
```

### Change Posting Schedule
Edit `config.py` posting times:
```python
POSTING_SCHEDULE = {
    "morning_time": "06:15",  # UTC time for morning posts
    "night_time": "20:45",    # UTC time for night posts
}
```

Then run the update script:
```bash
python3 update_workflow_schedule.py
git add .github/workflows/daily-posts.yml
git commit -m "Update posting schedule"
git push
```

### Adjust Font Sizes
Edit `config.py`:
```python
CAIRO_FONTS = {
    "arabic_verse": {"size": 60},    # Arabic text
    "translation": {"size": 45},     # English translation
    "tafsir": {"size": 42},          # Tafsir explanation
}
```

### Change Watermark
Edit `config.py`:
```python
WATERMARK = "@YourInstagramHandle"
```

## 🛠️ Technical Details

### Arabic Rendering
- **Cairo/Pango Engine**: Professional text rendering with perfect harakat
- **Amiri Font**: Traditional Arabic calligraphy with full diacritics
- **RTL Support**: Proper right-to-left text direction
- **No Rendering Errors**: Unlike PIL, Cairo handles complex Arabic perfectly

### Content Sources
- **Verses**: QuranAPI community wrapper (quranapi.pages.dev)
- **Translation**: Sahih International
- **Tafsir**: Tazkirul Quran (naturally concise, 700-1500 chars)
- **All content is API-sourced** (zero made-up content)

### Carousel Generation
- **Dynamic Slides**: 1-10 slides based on content length
- **Instagram Optimized**: 1080×1350px format
- **Smart Splitting**: Long content automatically split across slides
- **Navigation**: "Swipe →" indicators on each slide

### Caching & Performance
- Local caching to reduce API calls
- Cached data tracked in git for reliability
- Offline fallback for cached content
- Fast generation (~30 seconds per post)

## 📱 Testing Locally

### Test Image Generation
```bash
python3 generate_post_cairo.py
```
Check `output/` folder for generated images.

### Test Full Workflow (Posts to Instagram!)
```bash
python3 create_post.py
```
⚠️ This will post to your Instagram account.

### Verify Production Readiness
```bash
python3 verify_production.py
```

## 🤲 Sadaqah Jariyah

This project is Sadaqah Jariyah (ongoing charity). Every person who benefits from these Quranic reminders will bring reward to all involved.

**May Allah accept this effort and make it a means of guidance for the Ummah. Ameen.** 🤲

---

## 📄 License

Open source - Free to use for spreading the message of the Quran.

**Built with ❤️ for the sake of Allah** • Version 2.0 • Production Ready
