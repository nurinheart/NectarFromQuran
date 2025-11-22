"""
Create and post Quranic verse to Instagram
✅ Auto-fetches authentic tafsir from APIs (NEVER makes up content)
✅ Multi-API fallback system (Quran.com → AlQuran.cloud → Quran-API.ir)
✅ Posts to feed + shares to story with "New Post" text
✅ Auto-cleanup of old files (7 days)
✅ Dynamic captions with trendy hashtags
"""

from generate_post_cairo import QuranPostGeneratorCairo
from instagram_poster import InstagramPoster
from config import DEFAULT_THEME, POSTING_SCHEDULE
import os
import sys
import time
import random


def generate_dynamic_caption(verse_info):
    """
    Generate highly varied captions - never repetitive
    Uses verse number to ensure different caption each time
    """
    surah_name = verse_info.get('surah_name', 'Quran')
    surah_num = verse_info.get('surah_number', 1)
    ayah_num = verse_info.get('ayah_number', 1)
    reference = f"{surah_name} {surah_num}:{ayah_num}"
    
    # MASSIVE variety - 50+ different caption styles
    all_caption_styles = [
        # Simple & Direct
        f"{reference}\n\nSwipe to read the tafsir →",
        f"Reflecting on {reference} today 🌙",
        f"{reference}",
        f"From {surah_name}...\n\n{reference}",
        
        # Question-based (engaging)
        f"What does this verse mean to you?\n\n{reference}",
        f"Have you reflected on this today?\n\n{reference}",
        f"Ever thought about this verse?\n\n{reference}",
        
        # Time-based
        f"Today's reflection: {reference} 🌅",
        f"Morning reminder from {surah_name} ☀️\n\n{reference}",
        f"Tonight's verse: {reference} 🌙",
        f"Daily Quran: {reference}",
        
        # Emotional
        f"This verse... SubhanAllah �\n\n{reference}",
        f"The words of Allah ✨\n\n{reference}",
        f"Such a beautiful reminder 🤲\n\n{reference}",
        f"Alhamdulillah for this guidance 🙏\n\n{reference}",
        
        # Actionable
        f"Read this. Reflect on it. Apply it.\n\n{reference}",
        f"Swipe for the translation and tafsir →\n\n{reference}",
        f"Take a moment to understand this verse\n\n{reference}",
        f"Read slowly. Reflect deeply.\n\n{reference}",
        
        # Context
        f"From Surah {surah_name}, verse {ayah_num} 📖",
        f"Quran {surah_num}:{ayah_num}",
        f"Verse {ayah_num} of {surah_name}",
        
        # Contemplative  
        f"Pause. Read. Reflect.\n\n{reference}",
        f"A verse to ponder today 🤔\n\n{reference}",
        f"Let this sink in...\n\n{reference}",
        f"Food for thought 💭\n\n{reference}",
        
        # Community
        f"Sharing today's verse with you 💚\n\n{reference}",
        f"May this benefit us all\n\n{reference}",
        f"For everyone who needed this today\n\n{reference}",
        
        # Minimalist (most authentic)
        f"📖 {reference}",
        f"🌙 {reference}",
        f"✨ {reference}",
        
        # Reminder style
        f"A reminder from Allah\n\n{reference}",
        f"Words of wisdom from the Quran\n\n{reference}",
        f"Guidance from {surah_name}\n\n{reference}",
        
        # Neutral educational
        f"Understanding {reference}",
        f"Tafsir of {reference}",
        f"Exploring {reference} today",
        f"Learning from {reference}",
        
        # Personal
        f"My reflection on {reference}",
        f"Studying {reference} today",
        f"Notes on {reference}",
    ]
    
    # Use verse number as seed for consistency (same verse = same caption)
    # But different verses will get different captions
    caption_index = (surah_num * 1000 + ayah_num) % len(all_caption_styles)
    main_caption = all_caption_styles[caption_index]
    
    # Quran-focused, modest hashtag sets - rotated for variety
    hashtag_sets = [
        # Set 1: Core Quran & Islam
        "#Quran #HolyQuran #AlQuran #QuranDaily #QuranicVerses #Islam #Muslim #Allah #IslamicReminders #Deen #QuranicWisdom #Ayah #Surah #BookOfAllah",
        
        # Set 2: Daily Quran focus  
        "#DailyQuran #QuranQuotes #QuranReading #QuranRecitation #TilawatEQuran #Tafsir #QuranTranslation #LearnQuran #QuranStudy #IslamicKnowledge #QuranicTeachings",
        
        # Set 3: Muslim community & values
        "#Muslims #MuslimCommunity #Ummah #IslamicPost #MuslimLife #Alhamdulillah #SubhanAllah #MashaAllah #Taqwa #Iman #Faith #Sabr #IslamicQuotes",
        
        # Set 4: Learning & reflection
        "#LearnIslam #IslamicEducation #Tafsir #QuranicStudies #QuranMeaning #SeekKnowledge #IslamicTeachings #QuranReflection #UnderstandQuran #QuranicGuidance",
        
        # Set 5: Spiritual growth
        "#SpiritualGrowth #IslamicReminder #AllahsWords #DivinGuidance #QuranicHealing #PeaceInIslam #TrustInAllah #Dhikr #Dua #IslamicSpirituality #FaithInAllah",
    ]
    
    # Use verse number to pick hashtag set (consistent per verse)
    hashtag_index = (surah_num + ayah_num) % len(hashtag_sets)
    hashtags = hashtag_sets[hashtag_index]
    
    # Only add CTA if caption is very short (minimalist style)
    if len(main_caption) < 50:
        cta = "\n\nSwipe for translation & tafsir →"
        full_caption = main_caption + cta + "\n\n" + hashtags + "\n\n#NectarFromQuran"
    else:
        # No CTA for longer captions - cleaner look
        full_caption = main_caption + "\n\n" + hashtags + "\n\n#NectarFromQuran"
    
    return full_caption


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
    
    # Add random delay to mimic human behavior (30-180 seconds)
    delay = random.randint(30, 180)
    print(f"\n⏳ Random delay: {delay}s (mimics human behavior, avoids automation detection)")
    time.sleep(delay)
    
    try:
        # Initialize generator
        generator = QuranPostGeneratorCairo(DEFAULT_THEME)
        
        # Generate carousel slides
        print(f"\n📝 Generating post...")
        slide_paths = generator.generate_post()
        
        print(f"\n✅ Generated {len(slide_paths)} slides successfully!")
        
        # Post to Instagram
        print("\n📸 Posting to Instagram...")
        poster = InstagramPoster()
        
        # Generate dynamic caption based on verse theme
        verse_info = generator.get_verse_info()
        caption = generate_dynamic_caption(verse_info)
        
        # Post carousel to feed
        media_code = poster.post_carousel(slide_paths, caption)
        
        if media_code:
            print(f"\n✅ Successfully posted to feed!")
            print(f"🔗 Post Code: {media_code}")
            
            # Share to story with "New Post" text
            print(f"\n📤 Sharing to story...")
            post_url = f"https://www.instagram.com/p/{media_code}/"
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
