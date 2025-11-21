# 🚀 Quick Start - Deploy in 10 Minutes

Get your automated Quranic posts running on GitHub Actions FAST.

---

## ⚡ Speed Run (For Experienced Users)

```bash
# 1. Get Instagram session
python3 get_instagram_session.py
# Copy the session JSON output

# 2. Push to GitHub
git add .
git commit -m "Production ready"
git push

# 3. Add GitHub Secrets
# Go to: Settings → Secrets and variables → Actions → New repository secret
# Add: INSTAGRAM_USERNAME (your username)
# Add: INSTAGRAM_SESSION_DATA (the JSON from step 1)

# 4. Test manually
# Go to: Actions → Daily Quran Posts → Run workflow

# 5. Wait for scheduled posts at 06:00 & 21:00 UTC
```

Done! ✅

---

## 📖 Detailed 10-Minute Setup

### Step 1: Get Instagram Session (2 min)

```bash
cd /path/to/NectarFromQuran
python3 get_instagram_session.py
```

- Enter Instagram username
- Enter Instagram password
- Copy the entire JSON output (starts with `{` ends with `}`)

### Step 2: Configure (1 min)

Edit `config.py` only if needed:
- `WATERMARK = "@YourHandle"` - Change to your Instagram
- `DEFAULT_THEME = "elegant_black"` - Pick your theme
- `POSTING_SCHEDULE` times (default: 06:00 & 21:00 UTC)

### Step 3: Push to GitHub (2 min)

```bash
# If not initialized yet
git init
git add .
git commit -m "Initial commit - NectarFromQuran"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/NectarFromQuran.git
git push -u origin main
```

### Step 4: Add GitHub Secrets (3 min)

1. Go to your repo: `https://github.com/YOUR_USERNAME/NectarFromQuran`
2. Click: **Settings** (top menu)
3. Click: **Secrets and variables** → **Actions** (left sidebar)
4. Click: **New repository secret**

**Add Secret #1:**
- Name: `INSTAGRAM_USERNAME`
- Value: `your_instagram_username` (no @)
- Click: Add secret

**Add Secret #2:**
- Name: `INSTAGRAM_SESSION_DATA`
- Value: Paste the entire JSON from Step 1
- Click: Add secret

### Step 5: Test (2 min)

1. Go to **Actions** tab
2. Click **Daily Quran Posts** (left sidebar)
3. Click **Run workflow** button (right side)
4. Click **Run workflow** (green button)
5. Wait 5 minutes
6. Check your Instagram - new post should appear!

### Step 6: Go Live! (0 min)

Nothing to do! Workflow will auto-run at:
- 06:00 UTC (morning post)
- 21:00 UTC (night post)

---

## ✅ Verify It's Working

**Check GitHub Actions:**
- Actions tab → Should see green checkmarks ✅
- Click a run → View logs → Should say "Successfully posted"

**Check Instagram:**
- New carousel post in feed
- Story with first slide + "New Post" text
- Caption mentions "Tazkirul Quran"

**Check Files:**
- `posted_verses.json` updates after each post
- GitHub Actions logs show no errors

---

## 🔧 Quick Customization

### Change posting times:
Edit `.github/workflows/daily-posts.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'   # Change 6 to your hour (UTC)
  - cron: '0 21 * * *'  # Change 21 to your hour (UTC)
```

### Change theme:
Edit `config.py`:
```python
DEFAULT_THEME = "sage_cream"  # or "elegant_black" or "teal_gold"
```

### Change watermark:
Edit `config.py`:
```python
WATERMARK = "@YourHandle"
```

### Add more posts per day:
Edit `config.py`:
```python
POSTING_SCHEDULE = {
    "posts_per_day": 3,  # Increase to 3
}
```

Then add another cron in `.github/workflows/daily-posts.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'   # Morning
  - cron: '0 14 * * *'  # Afternoon (NEW)
  - cron: '0 21 * * *'  # Night
```

---

## 🐛 Common Issues

**"Instagram login error"**
→ Session expired. Re-run: `python3 get_instagram_session.py`
→ Update `INSTAGRAM_SESSION_DATA` secret in GitHub

**"No module named 'cairocffi'"**
→ GitHub Actions installs this automatically
→ If local error: `pip install -r requirements.txt`

**"Workflow not running"**
→ Check Actions tab → Workflow should be enabled (green dot)
→ GitHub Actions can delay up to 10 minutes
→ Test manually first (Run workflow button)

**Posts look wrong**
→ Test locally: `python3 generate_post_cairo.py`
→ Check `output/` folder
→ If good locally, issue is in GitHub Actions (check logs)

---

## 📚 Full Documentation

- **PRODUCTION_SETUP.md** - Complete setup guide
- **PRE_FLIGHT_CHECKLIST.md** - Pre-deployment checklist
- **config.py** - Full configuration options with examples
- **README.md** - Project overview

---

## 🎉 That's It!

You now have:
✅ Automated Instagram posts (2x daily)
✅ Authentic Quranic content (Tazkirul Quran)
✅ Beautiful carousel design (1-10 slides)
✅ Story sharing with post link
✅ Auto-cleanup (keeps last 7 days)
✅ Endless verse tracking (never repeats)

**Time to first post:** Next scheduled run (06:00 or 21:00 UTC)

**No computer needed:** Runs on GitHub's servers 24/7

**May your posts benefit the Ummah!** 🕌✨

---

## 💡 Pro Tips

1. **Test during off-hours** - First test won't notify followers
2. **Monitor first 24 hours** - Check logs for any issues
3. **Refresh session every 60 days** - Mark calendar reminder
4. **Keep `posted_verses.json` in git** - Preserves post history
5. **Use business account** - Better Instagram API stability

---

## 🚀 Ready? Let's Go!

Start with Step 1: `python3 get_instagram_session.py`

Questions? Check **PRODUCTION_SETUP.md** for detailed help.
