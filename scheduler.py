"""
Daily Scheduler for Automatic Instagram Posting
Posts 2 times daily at configured times (6 AM and 9 PM)
"""

import schedule
import time
import subprocess
import os
from datetime import datetime
from config import POSTING_SCHEDULE


def post_to_instagram():
    """Generate and post a new verse to Instagram"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"🕐 SCHEDULED POST: {timestamp}")
    print(f"{'='*60}\n")
    
    try:
        # Run the post generation and upload script
        result = subprocess.run(
            ["python3", "create_post.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ Post successful at {timestamp}")
            print(result.stdout)
        else:
            print(f"❌ Post failed at {timestamp}")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  Post timed out after 5 minutes at {timestamp}")
    except Exception as e:
        print(f"❌ Error during scheduled post: {e}")


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


def run_scheduler():
    """Set up and run the daily posting schedule"""
    morning_time = POSTING_SCHEDULE.get('morning_time', '06:00')
    night_time = POSTING_SCHEDULE.get('night_time', '21:00')
    
    print("="*60)
    print("🤖 NECTAR FROM QURAN - AUTOMATED SCHEDULER")
    print("="*60)
    print(f"📅 Schedule:")
    print(f"   Morning post: {morning_time}")
    print(f"   Night post:   {night_time}")
    print(f"   Cleanup:      Every day at midnight (7 day retention)")
    print("="*60)
    print("⏳ Scheduler is running... Press Ctrl+C to stop")
    print("="*60)
    
    # Schedule posts
    schedule.every().day.at(morning_time).do(post_to_instagram)
    schedule.every().day.at(night_time).do(post_to_instagram)
    
    # Schedule cleanup at midnight
    schedule.every().day.at("00:00").do(cleanup_old_files)
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Scheduler stopped by user")


if __name__ == "__main__":
    run_scheduler()
