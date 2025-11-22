#!/usr/bin/env python3
"""Test Instagram login and session management"""

import os
import sys

# Set test credentials (use your actual ones)
os.environ['INSTAGRAM_USERNAME'] = input("Enter Instagram username: ")
os.environ['INSTAGRAM_PASSWORD'] = input("Enter Instagram password: ")

from instagram_poster import InstagramPoster

try:
    print("\n" + "="*60)
    print("TESTING INSTAGRAM LOGIN")
    print("="*60)
    
    poster = InstagramPoster()
    
    print("\n✅ Login successful!")
    print("✅ Client is ready to post")
    
    # Test that client is actually logged in
    account = poster.client.account_info()
    print(f"✅ Verified: Logged in as @{account.username}")
    print(f"✅ User ID: {account.pk}")
    
    print("\n" + "="*60)
    print("SUCCESS - Instagram poster is ready!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
