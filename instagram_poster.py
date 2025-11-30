"""
Instagram Auto-Poster
Posts generated hadith images to Instagram automatically

ROBUST SESSION MANAGEMENT:
- Primary: Use session from INSTAGRAM_SESSION_DATA secret
- Fallback: Password login with session verification
- Auto-repair: Fix missing session fields
- Retry logic: Handle transient API failures
"""

import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired, TwoFactorRequired, ChallengeRequired,
    ClientError, ClientLoginRequired, PleaseWaitFewMinutes,
    RateLimitError, FeedbackRequired
)
from instagrapi.types import StoryLink
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class InstagramPoster:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.session_file = os.getenv('SESSION_FILE', 'instagram_session.json')
        self.client = None
        self._logged_in = False
        self._session_verified = False
        
        # Initialize client with proper settings
        self._init_client()
        
        # Perform login
        self.login()
    
    def _init_client(self):
        """Initialize Instagram client with proper device settings"""
        self.client = Client()
        
        # Set realistic device settings to avoid detection
        self.client.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "devitron",
            "model": "6T Dev",
            "cpu": "qcom",
            "version_code": "314665256"
        })
        
        # Set realistic user agent
        self.client.set_user_agent(
            "Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; 6T Dev; devitron; qcom; en_US; 314665256)"
        )
        
        # Set request timeouts
        self.client.request_timeout = 30
        
        # Add delay settings for more human-like behavior
        self.client.delay_range = [1, 3]
    
    def _verify_session_can_post(self):
        """Verify the session can actually perform actions, not just view"""
        try:
            # Try to get user info - this requires authenticated access
            user_id = self.client.user_id
            if not user_id:
                return False
            
            # Try to access the user's own profile (low-risk action)
            user_info = self.client.user_info(user_id)
            if user_info and user_info.username:
                print(f"✅ Session verified: Can access @{user_info.username}")
                return True
            return False
        except LoginRequired:
            print("⚠️  Session verification failed: LoginRequired")
            return False
        except Exception as e:
            print(f"⚠️  Session verification error: {e}")
            return False
    
    def _repair_session(self, session_dict):
        """Auto-repair session with all required fields"""
        repairs_made = []
        
        # Required fields that Instagram API expects
        required_fields = {
            'pinned_channels_info': {'pinned_channels_list': []},
            'cookies': {},
            'last_login': None,
            'device_settings': {
                "app_version": "269.0.0.18.75",
                "android_version": 26,
                "android_release": "8.0.0",
                "dpi": "480dpi",
                "resolution": "1080x1920",
                "manufacturer": "OnePlus",
                "device": "devitron",
                "model": "6T Dev",
                "cpu": "qcom",
                "version_code": "314665256"
            },
            'user_agent': "Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; 6T Dev; devitron; qcom; en_US; 314665256)",
            'country': 'US',
            'country_code': 1,
            'locale': 'en_US',
            'timezone_offset': -14400
        }
        
        for field, default_value in required_fields.items():
            if field not in session_dict:
                session_dict[field] = default_value
                repairs_made.append(field)
        
        if repairs_made:
            print(f"🔧 Auto-repaired session: Added {', '.join(repairs_made)}")
        
        return session_dict
    
    def login(self):
        """
        Robust login with multiple fallback strategies:
        1. Try existing session from env
        2. Verify session can perform actions
        3. If verification fails, do full password login
        4. After password login, verify before proceeding
        """
        session_data = os.getenv('INSTAGRAM_SESSION_DATA')
        
        # Strategy 1: Try existing session
        if session_data:
            if self._try_session_login(session_data):
                return
        
        # Strategy 2: Password login (session failed or doesn't exist)
        self._password_login()
    
    def _try_session_login(self, session_data):
        """Try to login with existing session data"""
        try:
            print("🔐 Attempting to reuse existing session...")
            session_dict = json.loads(session_data)
            
            # Auto-repair session
            session_dict = self._repair_session(session_dict)
            
            # Set the session
            self.client.set_settings(session_dict)
            
            # Try to use the session - don't call login, just verify
            if self._verify_session_can_post():
                self._logged_in = True
                self._session_verified = True
                print("✅ Session is valid and verified for posting!")
                return True
            else:
                print("⚠️  Session loaded but cannot perform actions")
                print("🔄 Falling back to password login...")
                # Re-initialize client for fresh login
                self._init_client()
                return False
                
        except json.JSONDecodeError:
            print("⚠️  Invalid session JSON format")
            self._init_client()
            return False
        except Exception as e:
            print(f"⚠️  Session load failed: {e}")
            self._init_client()
            return False
    
    def _password_login(self):
        """Perform full password login with verification"""
        if not self.username or not self.password:
            raise ValueError("❌ Instagram credentials not set! Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in GitHub secrets.")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔐 Password login attempt {attempt + 1}/{max_retries} as @{self.username}...")
                
                # Add random delay before login to appear more human
                if attempt > 0:
                    delay = random.uniform(5, 15)
                    print(f"⏳ Waiting {delay:.1f}s before retry...")
                    time.sleep(delay)
                
                # Perform login
                self.client.login(self.username, self.password)
                
                # Small delay after login
                time.sleep(random.uniform(2, 5))
                
                # Verify the session works for posting
                if self._verify_session_can_post():
                    self._logged_in = True
                    self._session_verified = True
                    print(f"✅ Login successful and verified for @{self.username}")
                    
                    # Save and display session for future use
                    self._save_and_display_session()
                    return
                else:
                    print(f"⚠️  Login succeeded but verification failed (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        self._init_client()  # Reset client for retry
                        continue
                    else:
                        # Last attempt - proceed anyway, let upload handle errors
                        print("⚠️  Proceeding without verification - upload will retry if needed")
                        self._logged_in = True
                        self._save_and_display_session()
                        return
                        
            except TwoFactorRequired:
                print("❌ 2FA is enabled. Please disable it temporarily or set up app-specific password.")
                raise
                
            except ChallengeRequired:
                print("⚠️  Instagram security challenge required.")
                print("Please login manually via Instagram app and try again in 24 hours.")
                raise
                
            except PleaseWaitFewMinutes as e:
                print(f"⚠️  Rate limited: {e}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(60, 120)
                    print(f"⏳ Waiting {wait_time:.0f}s before retry...")
                    time.sleep(wait_time)
                    self._init_client()
                else:
                    raise
                    
            except Exception as e:
                print(f"❌ Login attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    self._init_client()
                else:
                    raise
        
        raise Exception("❌ All login attempts failed")
    
    def _save_and_display_session(self):
        """Save session to file and display for GitHub secret update"""
        try:
            new_session = self.client.get_settings()
            self.client.dump_settings(self.session_file)
            
            print("\n" + "="*60)
            print("📋 COPY THIS TO INSTAGRAM_SESSION_DATA SECRET:")
            print("="*60)
            print(json.dumps(new_session, indent=2))
            print("="*60)
            print("\n⚠️  IMPORTANT: Update the INSTAGRAM_SESSION_DATA secret with the JSON above")
            print("   This session will be reused for ~2 weeks until it expires!")
            print("   Update at: https://github.com/nurinheart/NectarFromQuran/settings/secrets/actions\n")
        except Exception as e:
            print(f"⚠️  Could not save session: {e}")
    
    def _ensure_logged_in(self):
        """Ensure we're logged in before any action, with retry logic"""
        if not self._logged_in:
            self.login()
        
        # Quick check if session is still valid
        try:
            # Simple check - just get user_id (cached)
            if not self.client.user_id:
                print("⚠️  Session invalid, re-logging in...")
                self._init_client()
                self.login()
        except:
            print("⚠️  Session check failed, re-logging in...")
            self._init_client()
            self.login()
    
    def post_image(self, image_path, caption, hashtags=None):
        """Post single image to Instagram with retry logic"""
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"❌ Image not found: {image_path}")
        
        # Build full caption with hashtags
        full_caption = caption
        if hashtags:
            full_caption += "\n\n" + " ".join(hashtags)
        
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Ensure we're logged in
                self._ensure_logged_in()
                
                if attempt > 0:
                    print(f"📤 Retry {attempt + 1}/{max_retries}: Uploading to Instagram...")
                else:
                    print(f"📤 Uploading to Instagram...")
                print(f"   Image: {image_path}")
                print(f"   Caption length: {len(full_caption)} chars")
                
                # Add small random delay
                time.sleep(random.uniform(2, 5))
                
                # Upload photo
                media = self.client.photo_upload(
                    image_path,
                    caption=full_caption
                )
                
                print(f"✅ Posted successfully!")
                print(f"   Post ID: {media.pk}")
                print(f"   Link: https://www.instagram.com/p/{media.code}/")
                
                return media
                
            except (LoginRequired, ClientLoginRequired) as e:
                last_error = e
                print(f"⚠️  Login required (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    print("🔄 Re-authenticating...")
                    self._init_client()
                    self._logged_in = False
                    time.sleep(random.uniform(10, 30))
                    try:
                        self._password_login()
                    except Exception as login_err:
                        print(f"❌ Re-login failed: {login_err}")
                        
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                if 'login_required' in error_str:
                    print(f"⚠️  Login required error (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        self._init_client()
                        self._logged_in = False
                        time.sleep(random.uniform(10, 30))
                        try:
                            self._password_login()
                        except:
                            pass
                else:
                    print(f"❌ Upload failed (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(5, 15))
        
        print(f"❌ Image post failed after {max_retries} attempts: {last_error}")
        raise Exception(f"Failed to post: {last_error}")
    
    def test_connection(self):
        """Test if logged in and working"""
        try:
            self._ensure_logged_in()
            user_info = self.client.user_info_by_username(self.username)
            print(f"✅ Connected as @{user_info.username}")
            print(f"   Followers: {user_info.follower_count}")
            print(f"   Following: {user_info.following_count}")
            print(f"   Posts: {user_info.media_count}")
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def post_carousel(self, image_paths, caption):
        """
        Post multiple images as carousel with robust retry logic
        
        Handles:
        - Login required errors (re-authenticate and retry)
        - Rate limiting (wait and retry)
        - Transient failures (retry with backoff)
        """
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                from pathlib import Path
                from PIL import Image
                
                # Ensure we're logged in
                self._ensure_logged_in()
                
                # Convert to Path objects for verification
                paths = [Path(img) for img in image_paths]
                
                # Verify all files exist
                for path in paths:
                    if not path.exists():
                        print(f"❌ Image not found: {path}")
                        return None
                
                # Instagram carousels only support JPG format - convert PNG to JPG
                jpg_paths = []
                for path in paths:
                    if path.suffix.lower() == '.png':
                        jpg_path = path.with_suffix('.jpg')
                        # Convert PNG to JPG
                        img = Image.open(path)
                        # Convert RGBA to RGB (remove alpha channel)
                        if img.mode in ('RGBA', 'LA', 'P'):
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = rgb_img
                        img.save(jpg_path, 'JPEG', quality=95)
                        jpg_paths.append(jpg_path)
                    else:
                        jpg_paths.append(path)
                
                if attempt > 0:
                    print(f"📤 Retry {attempt + 1}/{max_retries}: Uploading carousel with {len(jpg_paths)} slides...")
                else:
                    print(f"📤 Uploading carousel with {len(jpg_paths)} slides...")
                
                # Add small random delay before upload to appear more human
                time.sleep(random.uniform(2, 5))
                
                # Upload as album/carousel
                media = self.client.album_upload(
                    paths=jpg_paths,
                    caption=caption
                )
                
                print(f"✅ Carousel posted successfully!")
                print(f"🔗 Media PK: {media.pk}")
                print(f"🔗 Media Code: {media.code}")
                print(f"🔗 Post URL: https://www.instagram.com/p/{media.code}/")
                
                # Cleanup temporary JPG files
                self._cleanup_temp_files(paths, jpg_paths)
                
                return media.code  # Return code (short URL slug) instead of PK
                
            except (LoginRequired, ClientLoginRequired) as e:
                last_error = e
                print(f"⚠️  Login required during upload (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    print("🔄 Re-authenticating...")
                    self._init_client()
                    self._logged_in = False
                    self._session_verified = False
                    
                    # Wait before retry
                    wait_time = random.uniform(10, 30)
                    print(f"⏳ Waiting {wait_time:.0f}s before retry...")
                    time.sleep(wait_time)
                    
                    # Force password login on retry
                    try:
                        self._password_login()
                    except Exception as login_err:
                        print(f"❌ Re-login failed: {login_err}")
                        continue
                else:
                    self._cleanup_temp_files(paths, jpg_paths)
                    
            except (RateLimitError, PleaseWaitFewMinutes) as e:
                last_error = e
                print(f"⚠️  Rate limited (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    wait_time = random.uniform(120, 300)  # 2-5 minutes
                    print(f"⏳ Waiting {wait_time:.0f}s before retry...")
                    time.sleep(wait_time)
                else:
                    self._cleanup_temp_files(paths, jpg_paths)
                    
            except FeedbackRequired as e:
                last_error = e
                print(f"❌ Instagram feedback required (spam detection): {e}")
                print("   This usually means Instagram flagged the action as spam.")
                print("   Try again in a few hours, or login manually to verify account.")
                self._cleanup_temp_files(paths, jpg_paths)
                return None  # Don't retry - this needs manual intervention
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Check if it's a login-related error
                if 'login_required' in error_str or 'login required' in error_str:
                    print(f"⚠️  Login required error (attempt {attempt + 1}): {e}")
                    
                    if attempt < max_retries - 1:
                        print("🔄 Re-authenticating with password...")
                        self._init_client()
                        self._logged_in = False
                        
                        wait_time = random.uniform(10, 30)
                        print(f"⏳ Waiting {wait_time:.0f}s before retry...")
                        time.sleep(wait_time)
                        
                        try:
                            self._password_login()
                        except Exception as login_err:
                            print(f"❌ Re-login failed: {login_err}")
                            continue
                else:
                    print(f"❌ Upload error (attempt {attempt + 1}): {e}")
                    import traceback
                    traceback.print_exc()
                    
                    if attempt < max_retries - 1:
                        wait_time = random.uniform(5, 15)
                        print(f"⏳ Waiting {wait_time:.0f}s before retry...")
                        time.sleep(wait_time)
                    else:
                        self._cleanup_temp_files(paths, jpg_paths)
        
        print(f"❌ Carousel post failed after {max_retries} attempts")
        print(f"   Last error: {last_error}")
        return None
    
    def _cleanup_temp_files(self, orig_paths, jpg_paths):
        """Cleanup temporary JPG files created during conversion"""
        try:
            for orig_path, jpg_path in zip(orig_paths, jpg_paths):
                if orig_path != jpg_path and jpg_path.exists():
                    jpg_path.unlink()
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    def share_to_story(self, image_path, post_url=None):
        """
        Share an image to Instagram Story with retry logic
        Optionally add a link sticker to the feed post
        
        Args:
            image_path: Path to image for story background
            post_url: URL to feed post (adds link sticker if provided)
        
        Returns:
            Story media pk or None if failed
        """
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                from pathlib import Path
                from PIL import Image, ImageDraw, ImageFont
                
                self._ensure_logged_in()
                
                image_path = Path(image_path)
                if not image_path.exists():
                    print(f"❌ Story image not found: {image_path}")
                    return None
                
                # Create proper story canvas (1080x1920 for Instagram stories)
                # Load original carousel image (1080x1350)
                carousel_img = Image.open(image_path)
                
                story_width = 1080
                story_height = 1920
                story_img = Image.new('RGB', (story_width, story_height), color=(0, 0, 0))
                
                # Center the carousel image vertically on story canvas
                y_offset = (story_height - carousel_img.height) // 2
                story_img.paste(carousel_img, (0, y_offset))
                
                # Add "Tap to view full post →" text at bottom with better styling
                draw = ImageDraw.Draw(story_img)
                
                try:
                    # Try Montserrat first (professional, clean)
                    font_large = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 100)
                    font_small = ImageFont.truetype("fonts/Montserrat-Regular.ttf", 75)
                except:
                    try:
                        # Fallback to Helvetica
                        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
                        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 75)
                    except:
                        # Last resort - system default
                        font_large = ImageFont.load_default()
                        font_small = ImageFont.load_default()
                
                # Main text
                main_text = "New Post"
                sub_text = "Tap to view"
                
                # Get text dimensions
                bbox_main = draw.textbbox((0, 0), main_text, font=font_large)
                main_width = bbox_main[2] - bbox_main[0]
                main_height = bbox_main[3] - bbox_main[1]
                
                bbox_sub = draw.textbbox((0, 0), sub_text, font=font_small)
                sub_width = bbox_sub[2] - bbox_sub[0]
                sub_height = bbox_sub[3] - bbox_sub[1]
                
                # Position at bottom with padding
                main_x = (story_width - main_width) // 2
                main_y = story_height - main_height - sub_height - 120
                
                sub_x = (story_width - sub_width) // 2
                sub_y = main_y + main_height + 20
                
                # Draw text with outline for visibility
                outline_color = (0, 0, 0)
                text_color = (255, 255, 255)
                
                # Draw main text with outline
                for adj_x in range(-3, 4):
                    for adj_y in range(-3, 4):
                        draw.text((main_x + adj_x, main_y + adj_y), main_text, font=font_large, fill=outline_color)
                draw.text((main_x, main_y), main_text, font=font_large, fill=text_color)
                
                # Draw sub text with outline
                for adj_x in range(-2, 3):
                    for adj_y in range(-2, 3):
                        draw.text((sub_x + adj_x, sub_y + adj_y), sub_text, font=font_small, fill=outline_color)
                draw.text((sub_x, sub_y), sub_text, font=font_small, fill=(200, 200, 200))
                
                # Save story image
                story_path = str(image_path).replace('.png', '_story.png')
                story_img.save(story_path)
                
                print(f"📤 Uploading to story (1080x1920)...")
                
                # Add small delay
                time.sleep(random.uniform(2, 5))
                
                # Upload to story
                if post_url:
                    link = StoryLink(webUri=post_url)
                    media = self.client.photo_upload_to_story(
                        path=story_path,
                        links=[link]
                    )
                else:
                    media = self.client.photo_upload_to_story(path=story_path)
                
                print(f"✅ Story posted successfully!")
                print(f"🔗 Story PK: {media.pk}")
                
                # Cleanup temp file
                if os.path.exists(story_path):
                    os.remove(story_path)
                
                return media.pk
                
            except (LoginRequired, ClientLoginRequired) as e:
                print(f"⚠️  Login required for story (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    self._init_client()
                    self._logged_in = False
                    time.sleep(random.uniform(10, 30))
                    try:
                        self._password_login()
                    except:
                        pass
                        
            except Exception as e:
                print(f"❌ Story post failed (attempt {attempt + 1}): {e}")
                import traceback
                traceback.print_exc()
                
                if attempt >= max_retries - 1:
                    return None
        
        return None
    
    def send_dm_to_followers(self, message, max_recipients=50):
        """
        Send DM to recent followers
        
        WARNING: Instagram heavily rate-limits DMs. Use sparingly!
        Recommended: max 20-30 DMs per day to avoid restrictions
        
        Args:
            message: Text message to send
            max_recipients: Maximum number of followers to message (default 50)
        
        Returns:
            Number of successful DMs sent
        """
        try:
            self._ensure_logged_in()
            print(f"📬 Sending DMs to up to {max_recipients} followers...")
            
            # Get follower list
            user_id = self.client.user_id_from_username(self.username)
            followers = self.client.user_followers(user_id, amount=max_recipients)
            
            successful = 0
            failed = 0
            
            for follower_id, follower_info in list(followers.items())[:max_recipients]:
                try:
                    # Send DM
                    self.client.direct_send(message, [follower_id])
                    successful += 1
                    print(f"✅ Sent to @{follower_info.username}")
                    
                    # Rate limiting: wait 2-3 seconds between messages
                    import time
                    import random
                    time.sleep(random.uniform(2, 3))
                    
                except Exception as e:
                    failed += 1
                    print(f"❌ Failed to send to @{follower_info.username}: {e}")
            
            print(f"\n📊 DM Summary: {successful} sent, {failed} failed")
            return successful
            
        except Exception as e:
            print(f"❌ DM broadcast failed: {e}")
            return 0
    
    def create_broadcast_channel(self, channel_name, description=""):
        """
        Create an Instagram broadcast channel
        
        Note: Broadcast channels are a newer Instagram feature.
        They allow one-to-many messaging (like Telegram channels)
        
        Args:
            channel_name: Name of the broadcast channel
            description: Channel description
        
        Returns:
            Channel ID if successful, None otherwise
        """
        try:
            print(f"📢 Creating broadcast channel: {channel_name}")
            
            # Note: instagrapi may not have full broadcast channel support yet
            # This is a placeholder for when the API catches up
            print("⚠️  Broadcast channels require Instagram app for now")
            print("   Create manually: Profile → Menu → Broadcast Channel")
            
            return None
            
        except Exception as e:
            print(f"❌ Channel creation failed: {e}")
            return None


def get_default_caption(hadith_text, source, category=None):
    """Generate a good default caption with hadith text"""
    caption = f'"{hadith_text}"\n\n'
    caption += f"— Prophet Muhammad ﷺ\n"
    caption += f"📖 {source} (Sahih)\n"
    caption += f"✓ Verified from 2+ authentic sources\n\n"
    
    if category:
        caption += f"#{category} "
    
    return caption


def get_default_hashtags():
    """Get default hashtags for hadith posts"""
    return [
        "#Hadith",
        "#Islam",
        "#IslamicQuotes",
        "#Muslim",
        "#ProphetMuhammad",
        "#IslamicReminders",
        "#SahihBukhari",
        "#Quran",
        "#Allah",
        "#Deen",
        "#IslamicPost",
        "#MuslimCommunity",
        "#IslamicKnowledge",
        "#Sunnah",
        "#Dawah"
    ]


if __name__ == "__main__":
    # Test the Instagram poster
    print("=" * 60)
    print("📱 INSTAGRAM AUTO-POSTER TEST")
    print("=" * 60)
    print()
    
    try:
        poster = InstagramPoster()
        poster.test_connection()
        
        print()
        print("✅ Instagram poster is ready!")
        print("💡 You can now use auto-posting in create_post.py")
        
    except Exception as e:
        print()
        print("❌ Setup incomplete. Please:")
        print("   1. Create .env file (copy from .env.example)")
        print("   2. Add your Instagram username and password")
        print("   3. Run this test again")
