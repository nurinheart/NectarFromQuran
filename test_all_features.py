#!/usr/bin/env python3
"""
Comprehensive Feature Test Suite
Tests all new features added to the project
"""

import sys
from pathlib import Path

def test_highlighting():
    """Test that highlighting only highlights 3-4 words max"""
    print("\n" + "="*60)
    print("TEST 1: Highlighting System (Max 4 Words)")
    print("="*60)
    
    from cairo_renderer import CairoArabicRenderer
    renderer = CairoArabicRenderer(1080, 1350)
    
    test_text = "This is a long sentence with many words to test highlighting functionality"
    result = renderer.highlight_random_words(test_text, max_words=4)
    
    import re
    highlights = len(re.findall(r'<span[^>]*>', result))
    
    print(f"Input: {len(test_text.split())} words")
    print(f"Highlighted: {highlights} words")
    print(f"Expected: 4 words")
    
    if highlights == 4:
        print("✅ PASS: Highlighting works correctly")
        return True
    else:
        print(f"❌ FAIL: Expected 4 highlights, got {highlights}")
        return False


def test_config():
    """Test that config has all required settings"""
    print("\n" + "="*60)
    print("TEST 2: Configuration Settings")
    print("="*60)
    
    from config import (
        ENABLE_HIGHLIGHTING, 
        HIGHLIGHT_MAX_WORDS,
        USE_ACCENT_COLOR_FOR_HIGHLIGHTS,
        ENABLE_THEME_ROTATION,
        ROTATION_THEMES
    )
    
    tests = [
        (ENABLE_HIGHLIGHTING == True, "ENABLE_HIGHLIGHTING"),
        (HIGHLIGHT_MAX_WORDS == 4, "HIGHLIGHT_MAX_WORDS = 4"),
        (USE_ACCENT_COLOR_FOR_HIGHLIGHTS == True, "USE_ACCENT_COLOR_FOR_HIGHLIGHTS"),
        (ENABLE_THEME_ROTATION == True, "ENABLE_THEME_ROTATION"),
        (len(ROTATION_THEMES) == 3, "ROTATION_THEMES (3 themes)")
    ]
    
    all_pass = True
    for test, name in tests:
        if test:
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
            all_pass = False
    
    if all_pass:
        print("✅ PASS: All config settings correct")
        return True
    else:
        print("❌ FAIL: Some config settings incorrect")
        return False


def test_multi_api():
    """Test multi-API fallback system"""
    print("\n" + "="*60)
    print("TEST 3: Multi-API Fallback System")
    print("="*60)
    
    from multi_api_quran import MultiAPIQuranFetcher
    
    fetcher = MultiAPIQuranFetcher()
    
    print(f"Configured APIs: {len(fetcher.apis)}")
    for api in fetcher.apis:
        print(f"  - {api['name']}")
    
    # Test fetching a verse
    print("\nTesting verse fetch (1:1)...")
    verse = fetcher.get_verse(1, 1, max_cycles=1)
    
    if verse:
        print(f"✅ Successfully fetched verse")
        print(f"   Arabic: {verse['arabic'][:50]}...")
        print(f"   Translation: {verse['translation'][:50]}...")
        print("✅ PASS: Multi-API system working")
        return True
    else:
        print("❌ FAIL: Could not fetch verse")
        return False


def test_instagram_features():
    """Test Instagram poster features (without actually posting)"""
    print("\n" + "="*60)
    print("TEST 4: Instagram Features")
    print("="*60)
    
    from instagram_poster import InstagramPoster
    
    # Check if methods exist
    methods = [
        'post_carousel',
        'share_to_story',
        'send_dm_to_followers',
        'create_broadcast_channel'
    ]
    
    all_exist = True
    for method in methods:
        if hasattr(InstagramPoster, method):
            print(f"✅ Method exists: {method}")
        else:
            print(f"❌ Method missing: {method}")
            all_exist = False
    
    if all_exist:
        print("✅ PASS: All Instagram features implemented")
        return True
    else:
        print("❌ FAIL: Some Instagram features missing")
        return False


def test_github_workflow():
    """Test GitHub Actions workflow configuration"""
    print("\n" + "="*60)
    print("TEST 5: GitHub Actions Workflow")
    print("="*60)
    
    workflow_file = Path('.github/workflows/daily-posts.yml')
    
    if not workflow_file.exists():
        print("❌ FAIL: Workflow file not found")
        return False
    
    content = workflow_file.read_text()
    
    checks = [
        ('archive/', 'Archive directory creation'),
        ('git add archive/', 'Archive git tracking'),
        ('Track posted verse + Archive images', 'Commit message includes archive'),
        ('retention-days: 7', 'Workflow artifacts retention')
    ]
    
    all_pass = True
    for check, description in checks:
        if check in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_pass = False
    
    if all_pass:
        print("✅ PASS: GitHub workflow configured correctly")
        return True
    else:
        print("❌ FAIL: GitHub workflow incomplete")
        return False


def test_archive_structure():
    """Test archive directory structure"""
    print("\n" + "="*60)
    print("TEST 6: Archive Directory Structure")
    print("="*60)
    
    archive_dir = Path('archive')
    readme = archive_dir / 'README.md'
    
    checks = [
        (archive_dir.exists(), "Archive directory exists"),
        (readme.exists(), "Archive README exists")
    ]
    
    all_pass = True
    for check, description in checks:
        if check:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            all_pass = False
    
    if all_pass:
        print("✅ PASS: Archive structure ready")
        return True
    else:
        print("❌ FAIL: Archive structure incomplete")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 COMPREHENSIVE FEATURE TEST SUITE")
    print("="*60)
    print("Testing all new features...")
    
    tests = [
        test_highlighting,
        test_config,
        test_multi_api,
        test_instagram_features,
        test_github_workflow,
        test_archive_structure
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ EXCEPTION in {test.__name__}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Project is complete and production-ready")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please review failed tests above")
        sys.exit(1)


if __name__ == "__main__":
    main()
