# Complete Fixes Applied - November 28, 2025

## NectarFromQuran Fixes

### 1. Instagram Login - Session Verification
**Issue**: Session was loading but then being rejected by aggressive verification step
- Removed `account_info()` verification after session load
- Session now loads and lets Instagram API fail naturally if invalid
- No more false "login_required" errors

### 2. Workflow Inputs Removed
**Issue**: GitHub Actions had manual inputs for posts_per_day and active_slot
- Removed `workflow_dispatch` inputs section
- Removed `POSTS_PER_DAY` and `ACTIVE_SLOT` environment variables
- **Config.py is now the single source of truth**

### 3. Time Verification Removed
**Issue**: Script was checking time and skipping posts
- Removed `should_post_now()` function entirely
- Script now always posts when cron runs
- No more "doesn't match posting slot" messages

## Sadaqah Fix Required

### Instagram Rate Limiting Issue
**Problem**: When Instagram blocks a post with "feedback_required":
1. Post fails
2. Hadith gets rolled back (not marked as posted)
3. Next run tries SAME hadith again
4. Creates infinite loop of same hadith

**Solution Needed**: 
- Mark hadith as "attempted" even if Instagram blocks it
- Skip to next hadith instead of retrying blocked one
- Add cooldown period or skip strategy for blocked hadiths

**Root Cause**: Instagram's anti-spam detection is blocking posts, but the rollback mechanism makes it retry infinitely.
