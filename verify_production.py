#!/usr/bin/env python3
"""
Production Readiness Verification Script
Run this before deploying to GitHub Actions
"""

import os
import sys
from pathlib import Path


def check_mark(passed):
    """Return check or X mark"""
    return "✅" if passed else "❌"


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def verify_files():
    """Verify all required files exist"""
    print_section("📁 FILE VERIFICATION")
    
    required_files = [
        'config.py',
        'create_post.py',
        'generate_post_cairo.py',
        'auto_tafsir_fetcher.py',
        'instagram_poster.py',
        'quran_api.py',
        'cairo_renderer.py',
        'font_manager.py',
        'requirements.txt',
        'get_instagram_session.py',
        '.github/workflows/daily-posts.yml',
        '.gitignore',
        'README.md',
        'QUICK_START.md',
    ]
    
    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        all_exist = all_exist and exists
        print(f"  {check_mark(exists)} {file}")
    
    return all_exist


def verify_fonts():
    """Verify font files exist"""
    print_section("🔤 FONT VERIFICATION")
    
    font_dirs = [
        'fonts/arabic/amiri',
        'fonts/arabic/noto',
        'fonts/arabic/scheherazade'
    ]
    
    fonts_ok = True
    for font_dir in font_dirs:
        exists = os.path.exists(font_dir)
        has_fonts = False
        
        if exists:
            ttf_files = list(Path(font_dir).rglob('*.ttf'))
            otf_files = list(Path(font_dir).rglob('*.otf'))
            has_fonts = len(ttf_files) > 0 or len(otf_files) > 0
        
        status = exists and has_fonts
        fonts_ok = fonts_ok and status
        
        font_count = len(ttf_files) + len(otf_files) if exists else 0
        print(f"  {check_mark(status)} {font_dir} ({font_count} fonts)")
    
    return fonts_ok


def verify_config():
    """Verify config.py settings"""
    print_section("⚙️  CONFIGURATION VERIFICATION")
    
    try:
        import config
        
        checks = {
            "DEFAULT_THEME exists": hasattr(config, 'DEFAULT_THEME'),
            "WATERMARK configured": hasattr(config, 'WATERMARK') and config.WATERMARK != "@YourHandle",
            "POSTING_SCHEDULE exists": hasattr(config, 'POSTING_SCHEDULE'),
            "HEADING_TEXTS configured": hasattr(config, 'HEADING_TEXTS'),
            "CAIRO_FONTS configured": hasattr(config, 'CAIRO_FONTS'),
        }
        
        all_ok = all(checks.values())
        
        for check, passed in checks.items():
            print(f"  {check_mark(passed)} {check}")
        
        # Show key values
        print(f"\n  Current Settings:")
        print(f"    Theme: {getattr(config, 'DEFAULT_THEME', 'NOT SET')}")
        print(f"    Watermark: {getattr(config, 'WATERMARK', 'NOT SET')}")
        
        schedule = getattr(config, 'POSTING_SCHEDULE', {})
        print(f"    Posts per day: {schedule.get('posts_per_day', 'NOT SET')}")
        print(f"    Morning time: {schedule.get('morning_time', 'NOT SET')}")
        print(f"    Night time: {schedule.get('night_time', 'NOT SET')}")
        
        return all_ok
        
    except ImportError as e:
        print(f"  ❌ Could not import config.py: {e}")
        return False


def verify_dependencies():
    """Verify Python dependencies can be imported"""
    print_section("📦 DEPENDENCY VERIFICATION")
    
    required_modules = [
        ('PIL', 'Pillow', True),
        ('requests', 'requests', True),
        ('instagrapi', 'instagrapi', True),
        ('cairocffi', 'cairocffi', False),  # OK if missing locally
        ('pangocffi', 'pangocffi', False),  # OK if missing locally
        ('pangocairocffi', 'pangocairocffi', False),  # OK if missing locally
    ]
    
    all_ok = True
    for module_name, package_name, required_local in required_modules:
        try:
            __import__(module_name)
            print(f"  ✅ {package_name}")
        except (ImportError, OSError):
            if required_local:
                print(f"  ❌ {package_name} (run: pip install -r requirements.txt)")
                all_ok = False
            else:
                print(f"  ⚠️  {package_name} (OK - GitHub Actions will install)")
    
    return all_ok


def verify_tafsir():
    """Verify tafsir fetcher is using Tazkirul Quran"""
    print_section("📖 TAFSIR SOURCE VERIFICATION")
    
    try:
        with open('auto_tafsir_fetcher.py', 'r') as f:
            content = f.read()
        
        checks = {
            "Uses Tazkirul Quran": 'Tazkirul' in content,
            "Uses QuranAPI wrapper": 'quranapi.pages.dev' in content,
            "Returns FULL content": 'FULL content' in content or 'NO SUMMARIZATION' in content,
        }
        
        all_ok = all(checks.values())
        
        for check, passed in checks.items():
            print(f"  {check_mark(passed)} {check}")
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Could not verify: {e}")
        return False


def verify_github_actions():
    """Verify GitHub Actions workflow"""
    print_section("🔄 GITHUB ACTIONS VERIFICATION")
    
    try:
        with open('.github/workflows/daily-posts.yml', 'r') as f:
            content = f.read()
        
        checks = {
            "Has schedule": 'schedule:' in content and 'cron:' in content,
            "Has workflow_dispatch": 'workflow_dispatch' in content,
            "Installs Cairo/Pango": 'libcairo2-dev' in content and 'libpango1.0-dev' in content,
            "Installs Arabic fonts": 'fonts-amiri' in content or 'fonts-noto' in content,
            "Uses Python 3.11+": 'python-version' in content and '3.11' in content,
            "Has secrets configured": 'INSTAGRAM_USERNAME' in content and 'INSTAGRAM_SESSION_DATA' in content,
        }
        
        all_ok = all(checks.values())
        
        for check, passed in checks.items():
            print(f"  {check_mark(passed)} {check}")
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Could not verify: {e}")
        return False


def verify_gitignore():
    """Verify .gitignore is properly configured"""
    print_section("🚫 GITIGNORE VERIFICATION")
    
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        checks = {
            "Excludes __pycache__": '__pycache__' in content,
            "Excludes output images": 'output/*.png' in content,
            "Excludes .env": '.env' in content,
            "Mentions cache tracking": 'posted_verses.json' in content or 'tafsir_cache' in content,  # Should mention these are tracked
        }
        
        all_ok = all(checks.values())
        
        for check, passed in checks.items():
            print(f"  {check_mark(passed)} {check}")
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Could not verify: {e}")
        return False


def test_generation():
    """Test if image generation works"""
    print_section("🎨 IMAGE GENERATION TEST")
    
    try:
        print("  Testing imports...")
        import config
        import quran_api
        import auto_tafsir_fetcher
        
        print(f"  ✅ config.py imports successfully")
        print(f"  ✅ quran_api.py imports successfully")
        print(f"  ✅ auto_tafsir_fetcher.py imports successfully")
        print(f"  💡 Run 'python3 generate_post_cairo.py' to test full generation")
        print(f"  💡 (Cairo imports will work on GitHub Actions)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        print(f"  💡 Fix errors before proceeding")
        return False


def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  🚀 PRODUCTION READINESS VERIFICATION")
    print("="*60)
    print("\nChecking if your system is ready for GitHub Actions deployment...")
    
    results = {
        "Files": verify_files(),
        "Fonts": verify_fonts(),
        "Config": verify_config(),
        "Dependencies": verify_dependencies(),
        "Tafsir": verify_tafsir(),
        "GitHub Actions": verify_github_actions(),
        "Gitignore": verify_gitignore(),
        "Generation": test_generation(),
    }
    
    # Summary
    print_section("📊 SUMMARY")
    
    all_passed = all(results.values())
    
    for category, passed in results.items():
        print(f"  {check_mark(passed)} {category}")
    
    print(f"\n{'='*60}")
    
    if all_passed:
        print("  ✅ ALL CHECKS PASSED!")
        print("="*60)
        print("\n🎉 Your system is production-ready!")
        print("\nNext steps:")
        print("  1. Run: python3 get_instagram_session.py")
        print("  2. Add GitHub secrets (see QUICK_START.md)")
        print("  3. Push to GitHub: git push")
        print("  4. Test: Actions → Daily Quran Posts → Run workflow")
        print("\n📖 See QUICK_START.md for detailed instructions.")
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED")
        print("="*60)
        print("\n⚠️  Fix the issues above before deploying.")
        print("\nCommon fixes:")
        print("  • Missing files: Ensure all files are present")
        print("  • Missing fonts: Check fonts/arabic/ directory")
        print("  • Dependencies: Run 'pip install -r requirements.txt'")
        print("  • Config: Update config.py with your settings")
        print("\n📖 See PRODUCTION_SETUP.md for help.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled")
        sys.exit(1)
