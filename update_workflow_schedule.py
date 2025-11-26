#!/usr/bin/env python3
"""
Update GitHub Actions workflow cron times to match config.py posting schedule.

This script reads the POSTING_SCHEDULE from config.py and updates the
.github/workflows/daily-posts.yml file to use the correct cron times.

Usage:
    python3 update_workflow_schedule.py
"""

import os
import re
import sys
from pathlib import Path

# Add current directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import POSTING_SCHEDULE
except ImportError as e:
    print(f"❌ Error importing config: {e}")
    sys.exit(1)

def time_to_cron(time_str):
    """Convert HH:MM time string to cron format (MM H * * *)"""
    hour, minute = map(int, time_str.split(':'))
    return f"{minute} {hour} * * *"

def update_workflow_cron():
    """Update the workflow file with cron times from config"""

    workflow_path = Path(".github/workflows/daily-posts.yml")

    if not workflow_path.exists():
        print(f"❌ Workflow file not found: {workflow_path}")
        return False

    # Read current workflow content
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get cron times from config
    morning_time = POSTING_SCHEDULE['morning_time']
    night_time = POSTING_SCHEDULE['night_time']

    morning_cron = time_to_cron(morning_time)
    night_cron = time_to_cron(night_time)

    print(f"📅 Config morning_time: {morning_time} → cron: {morning_cron}")
    print(f"📅 Config night_time: {night_time} → cron: {night_cron}")

    # Update cron entries in workflow
    # Pattern matches: - cron: 'XX X * * *'   # HH:MM UTC - Morning/Night post
    morning_pattern = r"(\s+- cron: ')\d+ \d+ \* \* \*('   # )\d{2}:\d{2}( UTC - Morning post)"
    night_pattern = r"(\s+- cron: ')\d+ \d+ \* \* \*('   # )\d{2}:\d{2}( UTC - Night post)"

    # Replace morning cron
    new_morning = rf"\g<1>{morning_cron}\g<2>{morning_time}\g<3>"
    content = re.sub(morning_pattern, new_morning, content)

    # Replace night cron
    new_night = rf"\g<1>{night_cron}\g<2>{night_time}\g<3>"
    content = re.sub(night_pattern, new_night, content)

    # Write updated content back
    with open(workflow_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Workflow cron times updated successfully!")
    print(f"   Morning: {morning_time} UTC ({morning_cron})")
    print(f"   Night: {night_time} UTC ({night_cron})")
    print("\n📝 Remember to commit and push these changes to update the schedule!")

    return True

if __name__ == "__main__":
    print("🔄 Updating workflow schedule from config.py...")
    success = update_workflow_cron()
    if success:
        print("\n🎯 Next steps:")
        print("   1. Review the changes: git diff .github/workflows/daily-posts.yml")
        print("   2. Commit: git add .github/workflows/daily-posts.yml")
        print("   3. Push: git commit -m 'Update workflow schedule to match config'")
        print("   4. Push: git push")
    else:
        sys.exit(1)