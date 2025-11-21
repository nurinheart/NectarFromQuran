"""
Instagram Auto-Poster
Posts generated hadith images to Instagram automatically
"""

import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired, ChallengeRequired
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InstagramPoster:
    def __init__(self):
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.session_file = os.getenv('SESSION_FILE', 'instagram_session.json')
        self.client = Client()
        
        # Load session if exists
        if os.path.exists(self.session_file):
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                print("✅ Logged in using saved session")
            except:
                print("⚠️  Session expired, logging in fresh...")
                self.login()
        else:
            self.login()
    
    def login(self):
        """Login to Instagram"""
        session_data = os.getenv('INSTAGRAM_SESSION_DATA')
        
        if session_data:
            try:
                print("🔐 Attempting to log in using session data...")
                session_dict = json.loads(session_data)
                self.client.set_settings(session_dict)
                self.client.login_by_sessionid(self.client.sessionid)
                print("✅ Logged in successfully using session data.")
                return
            except Exception as e:
                print(f"⚠️  Session login failed: {e}")
                print("   Please generate a new session.json and update the INSTAGRAM_SESSION_DATA secret.")
                raise
        
        if not self.username or not self.password:
            raise ValueError("❌ Instagram credentials not set! Please set INSTAGRAM_SESSION_DATA secret.")
        
        try:
            print(f"🔐 Logging in as @{self.username}...")
            self.client.login(self.username, self.password)
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully!")
            
        except TwoFactorRequired:
            code = input("Enter 2FA code: ")
            self.client.login(self.username, self.password, verification_code=code)
            self.client.dump_settings(self.session_file)
            print("✅ Logged in successfully with 2FA!")
            
        except ChallengeRequired:
            print("⚠️  Instagram security challenge required.")
            print("Please login manually via Instagram app and try again.")
            raise
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            raise
    
    def post_image(self, image_path, caption, hashtags=None):
        """Post image to Instagram"""
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"❌ Image not found: {image_path}")
        
        # Build full caption with hashtags
        full_caption = caption
        if hashtags:
            full_caption += "\n\n" + " ".join(hashtags)
        
        try:
            print(f"📤 Uploading to Instagram...")
            print(f"   Image: {image_path}")
            print(f"   Caption length: {len(full_caption)} chars")
            
            # Upload photo
            media = self.client.photo_upload(
                image_path,
                caption=full_caption
            )
            
            print(f"✅ Posted successfully!")
            print(f"   Post ID: {media.pk}")
            print(f"   Link: https://www.instagram.com/p/{media.code}/")
            
            return media
            
        except Exception as e:
            print(f"❌ Failed to post: {e}")
            raise
    
    def test_connection(self):
        """Test if logged in and working"""
        try:
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
        """Post multiple images as carousel"""
        try:
            from pathlib import Path
            
            # Convert paths to Path objects
            paths = [Path(img) for img in image_paths]
            
            # Verify all files exist
            for path in paths:
                if not path.exists():
                    print(f"❌ Image not found: {path}")
                    return None
            
            print(f"📤 Uploading carousel with {len(paths)} slides...")
            
            # Upload as album/carousel
            media = self.client.album_upload(
                paths=paths,
                caption=caption
            )
            
            print(f"✅ Carousel posted successfully!")
            print(f"🔗 Media PK: {media.pk}")
            return media.pk
            
        except Exception as e:
            print(f"❌ Carousel post failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def share_to_story(self, image_path, post_url=None):
        """
        Share an image to Instagram Story
        Optionally add a link sticker to the feed post
        
        Args:
            image_path: Path to image for story background
            post_url: URL to feed post (adds link sticker if provided)
        
        Returns:
            Story media pk or None if failed
        """
        try:
            from pathlib import Path
            from PIL import Image, ImageDraw, ImageFont
            
            image_path = Path(image_path)
            if not image_path.exists():
                print(f"❌ Story image not found: {image_path}")
                return None
            
            # Create story version with "New Post" text at bottom
            story_img = Image.open(image_path)
            draw = ImageDraw.Draw(story_img)
            
            # Add "New Post" text at bottom
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            except:
                font = ImageFont.load_default()
            
            text = "New Post ✨"
            # Get text bbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position at bottom center
            x = (story_img.width - text_width) // 2
            y = story_img.height - text_height - 80
            
            # Draw text with outline for visibility
            outline_color = (0, 0, 0)
            text_color = (255, 255, 255)
            
            # Draw outline
            for adj_x in range(-2, 3):
                for adj_y in range(-2, 3):
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=text_color)
            
            # Save modified story image
            story_path = str(image_path).replace('.png', '_story.png')
            story_img.save(story_path)
            
            print(f"📤 Uploading to story...")
            
            # Upload to story
            if post_url:
                # Add link sticker if post URL provided
                media = self.client.photo_upload_to_story(
                    path=Path(story_path),
                    links=[{"webUri": post_url}]
                )
            else:
                media = self.client.photo_upload_to_story(path=Path(story_path))
            
            print(f"✅ Story posted successfully!")
            print(f"🔗 Story PK: {media.pk}")
            
            # Cleanup temp file
            if os.path.exists(story_path):
                os.remove(story_path)
            
            return media.pk
            
        except Exception as e:
            print(f"❌ Story post failed: {e}")
            import traceback
            traceback.print_exc()
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
