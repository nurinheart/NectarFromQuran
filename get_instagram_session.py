#!/usr/bin/env python3
"""
Instagram Session Generator for GitHub Actions
Run this locally to get your session data for GitHub secrets
"""

from instagrapi import Client
import json
import sys


def get_session_data():
    """Get Instagram session data for GitHub Actions"""
    
    print("🔐 Instagram Session Generator")
    print("=" * 60)
    print("This script will generate session data for GitHub Actions")
    print("Your credentials are NOT stored - only session data")
    print("=" * 60)
    print()
    
    # Get credentials
    username = input("Instagram username: ").strip()
    password = input("Instagram password: ").strip()
    
    if not username or not password:
        print("\n❌ Username and password are required!")
        sys.exit(1)
    
    print(f"\n🔄 Logging in as @{username}...")
    
    try:
        # Initialize client
        cl = Client()
        
        # Login
        cl.login(username, password)
        
        print("✅ Login successful!")
        
        # Get session data
        session = cl.get_settings()
        session_json = json.dumps(session)
        
        # Display results
        print("\n" + "=" * 60)
        print("✅ SESSION DATA GENERATED")
        print("=" * 60)
        
        print("\n📋 Follow these steps:")
        print("\n1. Go to your GitHub repository")
        print("2. Click: Settings → Secrets and variables → Actions")
        print("3. Click: New repository secret")
        print("\n4. Add Secret #1:")
        print("   Name: INSTAGRAM_USERNAME")
        print(f"   Value: {username}")
        
        print("\n5. Add Secret #2:")
        print("   Name: INSTAGRAM_SESSION_DATA")
        print("   Value: (copy the JSON below)")
        
        print("\n" + "=" * 60)
        print("COPY THIS JSON (entire line):")
        print("=" * 60)
        print(session_json)
        print("=" * 60)
        
        print("\n⚠️  IMPORTANT SECURITY NOTES:")
        print("   • Keep this session data secure")
        print("   • Don't share it publicly")
        print("   • Sessions expire after ~60 days")
        print("   • Re-run this script when posts fail")
        
        print("\n✅ Setup complete! Ready for GitHub Actions.")
        print(f"📖 See PRODUCTION_SETUP.md for next steps.")
        
    except Exception as e:
        print(f"\n❌ Login failed: {e}")
        print("\nPossible solutions:")
        print("  1. Check username/password")
        print("  2. Disable 2FA temporarily")
        print("  3. Use Instagram app password")
        print("  4. Wait a few minutes and try again")
        sys.exit(1)


if __name__ == "__main__":
    try:
        get_session_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled")
        sys.exit(0)
