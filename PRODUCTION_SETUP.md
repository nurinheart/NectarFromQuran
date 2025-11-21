# 🚀 Production Setup Guide - NectarFromQuran

Complete guide to deploy automated Quranic verse posts with GitHub Actions.

---

## 📋 Prerequisites

- GitHub account
- Instagram business/creator account
- Basic familiarity with GitHub repositories

---

## 🔧 Step 1: GitHub Repository Setup

### 1.1 Push Code to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - NectarFromQuran automated posting system"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/NectarFromQuran.git

# Push to GitHub
git push -u origin main
```

---

## 🔐 Step 2: Configure Instagram Secrets

GitHub Actions needs your Instagram credentials to post. We'll store them as **encrypted secrets**.

### 2.1 Get Instagram Session Data

Run this script locally to get your session data:

```bash
python3 -c "
from instagrapi import Client
import json

# Login to Instagram
cl = Client()
username = input('Instagram username: ')
password = input('Instagram password: ')

try:
    cl.login(username, password)
    print('\n✅ Login successful!')
    
    # Get session data
    session = cl.get_settings()
    session_json = json.dumps(session)
    
    print('\n📋 Copy this session data:')
    print('=' * 60)
    print(session_json)
    print('=' * 60)
    
    print('\n⚠️  IMPORTANT: Keep this data secure!')
    print('Add it as INSTAGRAM_SESSION_DATA secret in GitHub.')
    
except Exception as e:
    print(f'❌ Login failed: {e}')
    print('Try: Check password, 2FA, or use app password')
"
```

### 2.2 Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

**Secret 1:**
- Name: `INSTAGRAM_USERNAME`
- Value: Your Instagram username (e.g., `nectarfromquran`)

**Secret 2:**
- Name: `INSTAGRAM_SESSION_DATA`
- Value: The JSON session data from step 2.1 (paste the entire output)

---

## ⏰ Step 3: Configure Posting Schedule

### 3.1 Edit `config.py`

```python
POSTING_SCHEDULE = {
    "morning_time": "06:00",  # Morning post time (UTC)
    "night_time": "21:00",    # Night post time (UTC)
    "posts_per_day": 2,       # Number of posts per day
    "cleanup_days": 7         # Keep files for 7 days
}
```

### 3.2 Adjust GitHub Actions Schedule

Edit `.github/workflows/daily-posts.yml`:

```yaml
on:
  schedule:
    # Adjust these times to match your POSTING_SCHEDULE
    - cron: '0 6 * * *'   # 06:00 UTC - Morning
    - cron: '0 21 * * *'  # 21:00 UTC - Night
```

**Cron Format:** `minute hour day month weekday`
- `0 6 * * *` = Every day at 06:00 UTC
- `0 21 * * *` = Every day at 21:00 UTC

**Time Zone Note:** GitHub Actions uses UTC. Convert your local time:
- EST: Add 5 hours
- PST: Add 8 hours
- GMT: Same as UTC

---

## 🎨 Step 4: Customize Your Posts

### 4.1 Theme Selection

Edit `config.py`:

```python
DEFAULT_THEME = "elegant_black"  # Options: "elegant_black", "sage_cream", "teal_gold"
```

### 4.2 Font Sizes

```python
CAIRO_FONTS = {
    "arabic_verse": {"size": 60},    # Arabic text
    "translation": {"size": 45},     # English translation
    "tafsir": {"size": 42},          # Tafsir explanation
    "heading": {"size": 40},         # Slide headings
    "reference": {"size": 30},       # Surah reference
}
```

### 4.3 Branding

```python
WATERMARK = "@YourHandle"  # Change to your Instagram handle

HEADING_TEXTS = {
    "arabic_slide": "Verse of Reflection",
    "translation_slide": "English Translation",
    "tafsir_slide": "Tazkirul Qur'an",
    "example_slide": "Reflection"
}
```

### 4.4 Visual Effects

```python
PATTERN_SETTINGS = {
    'grain_intensity': 0.3,   # Texture (0.0 = none, 0.3 = high)
    'grain_noise': 40,        # Grain detail (15-40)
}
```

---

## 🧪 Step 5: Test the System

### 5.1 Test Locally

```bash
# Generate a post (doesn't upload to Instagram)
python3 generate_post_cairo.py

# Check output folder
ls -la output/

# Full test with Instagram posting (CAREFUL - this posts to your account!)
python3 create_post.py
```

### 5.2 Test GitHub Actions Manually

1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **Daily Quran Posts** workflow
4. Click **Run workflow** → **Run workflow**
5. Watch the logs to ensure it completes successfully

---

## 🚦 Step 6: Go Live!

### 6.1 Enable Automated Posting

The workflow is now active! It will automatically:
- ✅ Post at scheduled times (06:00 & 21:00 UTC by default)
- ✅ Fetch authentic tafsir from QuranAPI (Tazkirul Quran)
- ✅ Generate beautiful carousel with 1-10 slides
- ✅ Post to Instagram feed
- ✅ Share first slide to story with "New Post" text
- ✅ Auto-cleanup old images after 7 days

### 6.2 Monitor Activity

**View Logs:**
1. Go to **Actions** tab in GitHub
2. Click on any workflow run
3. Click **post-quran** job
4. Expand steps to see detailed logs

**Check for Errors:**
- ❌ If workflow fails, check the logs
- Common issues: Instagram session expired, font missing, API down
- Re-run failed workflows by clicking **Re-run all jobs**

---

## 🔄 Step 7: Maintenance

### 7.1 Refresh Instagram Session (Every 60 days)

Instagram sessions expire. When posts fail:

1. Run the session script again (Step 2.1)
2. Update `INSTAGRAM_SESSION_DATA` secret in GitHub
3. Re-run the workflow

### 7.2 Update Dependencies

```bash
# Update Python packages locally
pip install --upgrade -r requirements.txt

# Test locally
python3 generate_post_cairo.py

# Push updates
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### 7.3 Monitor Posted Verses

The system tracks posted verses in `posted_verses.json`:

```bash
# View posted verses
cat posted_verses.json

# Reset to start over (CAREFUL - will repost old verses)
rm posted_verses.json
git add posted_verses.json
git commit -m "Reset posted verses"
git push
```

---

## 📊 System Features

✅ **Authentic Content**
- Fetches Quranic verses from API (Sahih International translation)
- Fetches Tazkirul Quran tafsir (naturally concise, 700-1500 chars)
- NEVER makes up religious content
- Only generates reflection/example (no API exists)

✅ **Intelligent Post Generation**
- Dynamic 1-10 slides based on content length
- Perfect Arabic rendering with harakat using Cairo/Pango
- Responsive text splitting (long verses → multiple slides)
- Professional design with Product Sans font

✅ **Instagram Optimization**
- Carousel posts (1080x1350px Instagram format)
- Auto-share to story with post link
- Optimized captions with hashtags
- Navigation arrows ("Swipe →")

✅ **Automation**
- GitHub Actions (runs on GitHub's servers, not your computer)
- Scheduled posting (2x daily by default)
- Auto-cleanup (deletes old images after 7 days)
- Endless verse tracking (never repeats)

---

## 🛠️ Troubleshooting

### Problem: Workflow fails with "Instagram login error"

**Solution:**
1. Session expired - refresh it (Step 2.1)
2. Update `INSTAGRAM_SESSION_DATA` secret
3. Re-run workflow

### Problem: Arabic text not rendering properly

**Solution:**
GitHub Actions installs fonts automatically. If issues persist:
1. Check workflow logs for font installation errors
2. Verify `fonts-amiri` package installed
3. Test locally first: `python3 generate_post_cairo.py`

### Problem: Workflow doesn't run at scheduled time

**Solution:**
1. GitHub Actions can delay up to 10 minutes
2. Check if workflow is enabled (Actions tab → Enable workflow)
3. Verify cron syntax is correct
4. Test manually first (Run workflow button)

### Problem: Posts are too long (>10 slides)

**Solution:**
Tazkirul Quran is naturally concise. If hitting 10-slide limit:
1. Check if verse is extremely long (e.g., 2:282)
2. System auto-splits and respects 10-slide limit
3. Some very long verses may need manual handling

### Problem: API rate limiting

**Solution:**
1. System caches tafsir to avoid repeated calls
2. Delete `tafsir_cache.json` and `quran_cache.json` only if needed
3. QuranAPI has no known rate limits

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `config.py` | Main configuration (theme, fonts, schedule) |
| `create_post.py` | Main script (generate + post + story + cleanup) |
| `generate_post_cairo.py` | Image generation with Cairo rendering |
| `auto_tafsir_fetcher.py` | Fetches Tazkirul Quran from QuranAPI |
| `instagram_poster.py` | Instagram API integration |
| `posted_verses.json` | Tracks posted verses (git tracked) |
| `.github/workflows/daily-posts.yml` | GitHub Actions automation |

---

## 🔒 Security Best Practices

1. ✅ **Never commit secrets** to git
2. ✅ Use GitHub encrypted secrets for credentials
3. ✅ Rotate Instagram session every 60 days
4. ✅ Use a dedicated Instagram account (not personal)
5. ✅ Enable 2FA on GitHub
6. ✅ Review workflow logs regularly

---

## 📈 Scaling Up

Want more posts per day?

1. Edit `config.py`:
   ```python
   POSTING_SCHEDULE = {
       "posts_per_day": 3,  # Increase to 3
   }
   ```

2. Add more cron schedules in `.github/workflows/daily-posts.yml`:
   ```yaml
   schedule:
     - cron: '0 6 * * *'   # Morning
     - cron: '0 14 * * *'  # Afternoon (NEW)
     - cron: '0 21 * * *'  # Night
   ```

3. Test locally first!

---

## 🎉 You're All Set!

Your automated Quranic verse posting system is now live! 

The system will:
- 🕌 Post authentic Quranic wisdom 2x daily
- 📱 Share beautiful carousel posts (1-10 slides)
- 📖 Include Tazkirul Quran tafsir (FULL content)
- 🌟 Auto-share to story
- 🧹 Clean up old files automatically

**May Allah accept this effort and make it a source of benefit for the Ummah.** 🤲

---

## 📞 Support

For issues or questions:
1. Check logs in GitHub Actions
2. Review this guide
3. Test locally before debugging workflow
4. Check API status: https://quranapi.pages.dev/

**Remember:** The system follows the strict rule of NEVER making up Islamic content - everything comes from authentic APIs! 🕊️
