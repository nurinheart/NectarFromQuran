"""
Create and post Quranic verse to Instagram
✅ Auto-fetches authentic tafsir from APIs (NEVER makes up content)
✅ Posts to feed + shares to story with "New Post" text
✅ Auto-cleanup of old files (7 days)
"""

from generate_post_cairo import QuranPostGeneratorCairo
from instagram_poster import InstagramPoster
from config import DEFAULT_THEME, POSTING_SCHEDULE
import os
import sys
import time


def cleanup_old_files():
    """Delete generated images older than configured days"""
    cleanup_days = POSTING_SCHEDULE.get('cleanup_days', 7)
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        return
    
    print(f"\n🧹 Running cleanup (files older than {cleanup_days} days)...")
    
    now = time.time()
    cutoff = now - (cleanup_days * 24 * 60 * 60)
    deleted_count = 0
    
    try:
        for filename in os.listdir(output_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(output_dir, filename)
                file_age = os.path.getmtime(filepath)
                
                if file_age < cutoff:
                    try:
                        os.remove(filepath)
                        deleted_count += 1
                        print(f"  🗑️  Deleted: {filename}")
                    except Exception as e:
                        print(f"  ⚠️  Could not delete {filename}: {e}")
        
        if deleted_count > 0:
            print(f"✅ Cleanup complete: {deleted_count} files deleted")
        else:
            print(f"✅ Cleanup complete: No old files to delete")
            
    except Exception as e:
        print(f"❌ Cleanup error: {e}")


def main():
    print("🕌 NectarFromQuran - Daily Quran Post Generator")
    print("=" * 60)
    
    try:
        # Initialize generator
        generator = QuranPostGeneratorCairo(DEFAULT_THEME)
        
        # Generate carousel slides
        print(f"\n📝 Generating post...")
        slide_paths = generator.generate_post()
        
        print(f"\n✅ Generated {len(slide_paths)} slides successfully!")
        
        # Post to Instagram
        print("\n� Posting to Instagram...")
        poster = InstagramPoster()
        
        # Create caption
        caption = f"""Daily wisdom from the Quran ✨

    Swipe through for:
• Arabic text with harakat
• Translation (Sahih International)
• Tazkirul Quran explanation
• Practical reflection

#quran #islam #islamicreminder #dailyquran #quranicwisdom #nectarfromquran #tafsir #islamicquotes #muslimlife"""
        
        # Post carousel to feed
        media_pk = poster.post_carousel(slide_paths, caption)
        
        if media_pk:
            print(f"\n✅ Successfully posted to feed!")
            print(f"🔗 Post ID: {media_pk}")
            
            # Share to story with "New Post" text
            print(f"\n📤 Sharing to story...")
            post_url = f"https://www.instagram.com/p/{media_pk}/"
            story_pk = poster.share_to_story(slide_paths[0], post_url)
            
            if story_pk:
                print(f"✅ Shared to story!")
                print(f"🔗 Story ID: {story_pk}")
            
            # Cleanup old files
            cleanup_old_files()
            
            print(f"\n🎉 All done! Check @nectarfromquran")
            sys.exit(0)
        else:
            print("\n❌ Failed to post to Instagram")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
