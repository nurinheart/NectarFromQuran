# GitHub Secrets Setup (One-Time)

## Required Secrets

Go to: https://github.com/nurinheart/NectarFromQuran/settings/secrets/actions

### 1. INSTAGRAM_USERNAME
- Value: Your Instagram username (without @)
- Example: `nectarfromquran`

### 2. INSTAGRAM_PASSWORD  
- Value: Your Instagram password
- **IMPORTANT**: Use a strong, unique password
- Consider enabling app-specific password if available

### 3. INSTAGRAM_SESSION_DATA (Optional - for faster login)
- If session expires, system will auto-generate new one using username/password
- You can leave this empty or delete it - system will work with just username/password

## How It Works

**OLD WAY (Manual):**
- Session expires every few weeks
- You had to manually run `generate_session.py`
- Copy/paste to GitHub secrets
- Pain in the ass

**NEW WAY (Automatic):**
1. System tries session login first (fast)
2. If session expired → automatically logs in with username/password
3. Generates new session and prints it in logs
4. Posts successfully ✅
5. (Optional) You can copy new session from logs to update secret for faster future logins

## Setup Steps

1. **Add Username**: 
   - Secret name: `INSTAGRAM_USERNAME`
   - Value: `nectarfromquran` (or your username)

2. **Add Password**:
   - Secret name: `INSTAGRAM_PASSWORD`  
   - Value: Your Instagram password

3. **Done!** System will handle session renewal automatically.

## Security Notes

- ✅ Secrets are encrypted by GitHub
- ✅ Never visible in logs or code
- ✅ Only accessible to your workflows
- ✅ Can be rotated anytime
- ⚠️ Disable 2FA temporarily (or use app password)
- ⚠️ If Instagram challenges you, wait 24 hours

## Troubleshooting

**"Login failed"**: 
- Check username/password are correct
- Disable 2FA temporarily
- Login manually via Instagram app first
- Wait 24 hours if account flagged

**"Challenge required"**:
- Instagram wants manual verification
- Login via app/browser manually
- Wait 24-48 hours
- Try again

**"Session keeps expiring"**:
- This is normal! System will auto-renew now
- No action needed from you

## Test It

After adding secrets, test immediately:
1. Go to Actions tab
2. Click "Daily Quran Posts"
3. Click "Run workflow" → "Run workflow"
4. Watch it work! Should post within 5 minutes
