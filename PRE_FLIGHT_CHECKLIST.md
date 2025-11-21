# ✈️ Pre-Flight Checklist - Production Deployment

Use this checklist before deploying to production with GitHub Actions.

---

## 📋 Configuration Checklist

### ✅ 1. Config File (`config.py`)

- [ ] `DEFAULT_THEME` is set to your preferred theme
- [ ] `WATERMARK` has your Instagram handle (e.g., `@NectarFromQuran`)
- [ ] `POSTING_SCHEDULE` times match your needs:
  - [ ] `morning_time` is correct (format: `"HH:MM"`)
  - [ ] `night_time` is correct (format: `"HH:MM"`)
  - [ ] `posts_per_day` is 2 (or your preference)
  - [ ] `cleanup_days` is 7 (or your preference)

### ✅ 2. GitHub Actions (`/.github/workflows/daily-posts.yml`)

- [ ] Cron schedule matches `POSTING_SCHEDULE` (converted to UTC)
- [ ] System dependencies include Cairo, Pango, and Arabic fonts
- [ ] Python version is 3.11 or higher

### ✅ 3. Instagram Caption (`create_post.py`)

- [ ] Caption mentions "Tazkirul Quran" (not Ibn Kathir)
- [ ] Hashtags are relevant to your account
- [ ] Caption reflects your branding

---

## 🔐 Secrets Checklist

### ✅ 4. Instagram Authentication

- [ ] Run `python3 get_instagram_session.py` locally
- [ ] Copy session JSON successfully
- [ ] Added `INSTAGRAM_USERNAME` secret to GitHub
- [ ] Added `INSTAGRAM_SESSION_DATA` secret to GitHub
- [ ] Secrets are set to "Repository" scope (not environment)

**Verify secrets exist:**
1. Go to GitHub repository
2. Settings → Secrets and variables → Actions
3. Should see: `INSTAGRAM_USERNAME` and `INSTAGRAM_SESSION_DATA`

---

## 🧪 Testing Checklist

### ✅ 5. Local Testing

- [ ] `python3 generate_post_cairo.py` runs without errors
- [ ] Check `output/` folder has generated images
- [ ] Images have correct Arabic text (check harakat)
- [ ] Images have correct theme/branding
- [ ] Text is readable and not cut off
- [ ] All slides look professional

### ✅ 6. Tafsir Verification

- [ ] Run test: `python3 -c "from auto_tafsir_fetcher import AutoTafsirFetcher; f = AutoTafsirFetcher(); print(f.fetch_tafsir(1, 1))"`
- [ ] Verify output says "Tazkirul Quran (FULL content)"
- [ ] Verify tafsir length is 700-1500 characters (reasonable)
- [ ] No summarization happening (full content preserved)

### ✅ 7. Instagram Integration Test (CAREFUL!)

**Warning:** This will post to your Instagram account!

- [ ] Have test Instagram account ready (recommended)
- [ ] Or test during off-hours
- [ ] Run: `python3 create_post.py`
- [ ] Verify post appears on Instagram feed
- [ ] Verify story was created with "New Post" text
- [ ] Check all slides display correctly
- [ ] Verify caption is correct

### ✅ 8. GitHub Actions Test

- [ ] Push code to GitHub
- [ ] Go to Actions tab
- [ ] Click "Daily Quran Posts" workflow
- [ ] Click "Run workflow" → "Run workflow"
- [ ] Wait for completion (5-10 minutes)
- [ ] Check logs for errors
- [ ] Verify post appeared on Instagram
- [ ] Download artifacts to review generated images

---

## 📁 File Checklist

### ✅ 9. Required Files Present

- [ ] `config.py` (configuration)
- [ ] `create_post.py` (main script)
- [ ] `generate_post_cairo.py` (image generation)
- [ ] `auto_tafsir_fetcher.py` (tafsir fetching)
- [ ] `instagram_poster.py` (Instagram API)
- [ ] `quran_api.py` (Quran API integration)
- [ ] `cairo_renderer.py` (Cairo text rendering)
- [ ] `font_manager.py` (font handling)
- [ ] `requirements.txt` (dependencies)
- [ ] `.github/workflows/daily-posts.yml` (automation)

### ✅ 10. Fonts Present

- [ ] `fonts/arabic/amiri/` exists
- [ ] `fonts/arabic/noto/` exists
- [ ] `fonts/arabic/scheherazade/` exists
- [ ] At least one Arabic font `.ttf` file exists
- [ ] Test: `ls -la fonts/arabic/*/`

---

## 🔄 Version Control Checklist

### ✅ 11. Git Setup

- [ ] `.gitignore` excludes sensitive files:
  - [ ] `*.pyc` and `__pycache__/`
  - [ ] `.env` (if used)
  - [ ] `venv/` or `.venv/`
  - [ ] But INCLUDES `posted_verses.json` (needed for tracking)
- [ ] All changes committed
- [ ] Pushed to GitHub main branch

### ✅ 12. What Gets Tracked

**Should be in git:**
- ✅ `posted_verses.json` (tracks posted verses)
- ✅ `tafsir_cache.json` (reduces API calls)
- ✅ `quran_cache.json` (reduces API calls)
- ✅ All `.py` files
- ✅ All config files
- ✅ Fonts folder

**Should NOT be in git:**
- ❌ `.env` (if you use one)
- ❌ `output/*.png` (temporary files)
- ❌ Session credentials (use GitHub secrets)
- ❌ `__pycache__/` folders

---

## 🚦 Launch Checklist

### ✅ 13. Pre-Launch

- [ ] All above tests passed
- [ ] Instagram account is ready (has profile pic, bio, etc.)
- [ ] Account is set to Public (for story shares to work)
- [ ] You're comfortable with automated posting
- [ ] Backup of `posted_verses.json` exists (if you want to preserve history)

### ✅ 14. Launch

- [ ] Workflow is enabled (Actions tab → Enable workflow if disabled)
- [ ] First scheduled run will happen at next cron time
- [ ] Or trigger manually: Actions → Run workflow

### ✅ 15. Post-Launch Monitoring (First 24 Hours)

- [ ] Check GitHub Actions logs after first run
- [ ] Verify post appeared on Instagram at scheduled time
- [ ] Check story was created
- [ ] Review generated images for quality
- [ ] Check error logs (should be none)
- [ ] Monitor second scheduled post

---

## 🎯 Success Criteria

Your system is production-ready when:

✅ **Local tests pass** - Images generate correctly
✅ **Manual GitHub Actions run succeeds** - Workflow completes without errors
✅ **Instagram post appears** - Carousel and story created
✅ **Content is authentic** - Tazkirul Quran tafsir shown in full
✅ **Schedule works** - Posts appear at configured times
✅ **Monitoring setup** - You can view logs and troubleshoot

---

## 🚨 Red Flags - DO NOT LAUNCH IF:

❌ Local tests fail or produce errors
❌ GitHub Actions manual run fails
❌ Instagram session expired (fix first)
❌ Missing required fonts (Arabic won't render)
❌ `posted_verses.json` not being tracked by git (will reset on each run)
❌ Secrets not configured in GitHub
❌ Cron times don't match your config

---

## 📞 If Something Goes Wrong

**Workflow fails:**
1. Check GitHub Actions logs (Actions tab → Click failed run)
2. Look for error messages (usually Instagram session or font issue)
3. Fix locally first, then push
4. Re-run failed workflow

**Instagram session expired:**
1. Run `python3 get_instagram_session.py`
2. Update `INSTAGRAM_SESSION_DATA` secret
3. Re-run workflow

**Wrong content posted:**
1. Stop workflow immediately (Actions → Disable workflow)
2. Fix content locally
3. Test: `python3 create_post.py`
4. Push fixes
5. Re-enable workflow

**Posts not appearing:**
1. Check GitHub Actions logs - did workflow run?
2. Check Instagram app - sometimes delayed
3. Verify secrets are correct
4. Check if account has posting restrictions

---

## ✅ Final Check

Read this out loud:

> "I have tested locally, configured GitHub secrets, verified the workflow runs successfully, and confirmed posts appear on Instagram. I understand this will post automatically at scheduled times. I'm ready to launch."

**If yes to all:** 🚀 **GO FOR LAUNCH!**

**If no to any:** 🛑 Go back and complete that section.

---

**May your automated posts benefit the Ummah!** 🕌✨
