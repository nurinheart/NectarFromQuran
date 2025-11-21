"""
Create and post Quranic verse to Instagram
✅ Auto-fetches authentic tafsir from APIs (NEVER makes up content)
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
    Generate dynamic, engaging captions with trendy hashtags
    Changes based on verse theme for variety
    """
    theme = verse_info.get('theme', 'Guidance')
    surah_name = verse_info.get('surah_name', 'Quran')
    reference = f"{surah_name} {verse_info.get('surah_number', '')}:{verse_info.get('ayah_number', '')}"
    
    # Theme-based caption hooks (trendy and engaging)
    caption_hooks = {
        'Mercy': [
            f"When you need a reminder of Allah's infinite mercy... 🤲\n\n{reference}",
            f"This verse hits different when you realize Allah's mercy is unlimited 💚\n\n{reference}",
            f"POV: You're feeling hopeless but then you read this verse 🌙\n\n{reference}",
            f"Allah's mercy > your mistakes. Remember this. ✨\n\n{reference}",
        ],
        'Patience': [
            f"The patience reminder we all needed today 🕊️\n\n{reference}",
            f"When life tests you, remember this verse 💪\n\n{reference}",
            f"POV: You're about to lose patience, then you remember... 🌸\n\n{reference}",
            f"This is your sign to keep going. Trust the process. 🌟\n\n{reference}",
        ],
        'Gratitude': [
            f"Daily gratitude check ✅ What are you thankful for today?\n\n{reference}",
            f"This verse will change how you see your blessings 🙏\n\n{reference}",
            f"Alhamdulillah for everything. Even the struggles. 💛\n\n{reference}",
            f"The gratitude mindset shift we all need 🌻\n\n{reference}",
        ],
        'Prayer': [
            f"Your Salah matters more than you think 🤲\n\n{reference}",
            f"This verse about prayer will hit your soul differently 🕌\n\n{reference}",
            f"POV: You almost skipped Fajr, then remembered this... 🌅\n\n{reference}",
            f"The power of Salah explained in one verse ✨\n\n{reference}",
        ],
        'Faith': [
            f"Faith check: This verse will strengthen your Iman 💚\n\n{reference}",
            f"When you doubt, read this. When you believe, read it again 🌙\n\n{reference}",
            f"This is the Iman boost you were looking for today ✨\n\n{reference}",
            f"Your faith journey starts here 🌟\n\n{reference}",
        ],
        'Guidance': [
            f"The guidance you've been seeking 🧭\n\n{reference}",
            f"Allah's roadmap for life in one verse 🌙\n\n{reference}",
            f"Lost? Read this. Found? Read it anyway. 💫\n\n{reference}",
            f"This verse is the answer to your du'a 🤲\n\n{reference}",
        ],
    }
    
    # Get hooks for this theme, fallback to Guidance if theme not found
    hooks = caption_hooks.get(theme, caption_hooks['Guidance'])
    main_caption = random.choice(hooks)
    
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
    
    # Pick random hashtag set for variety
    hashtags = random.choice(hashtag_sets)
    
    # Add swipe call-to-action
    cta = "\n\n📖 Swipe for translation, tafsir & practical reflection"
    
    # Combine all parts
    full_caption = main_caption + cta + "\n\n" + hashtags + "\n\n#NectarFromQuran"
    
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
