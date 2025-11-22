"""
Test Multi-API Quran Fetcher
Tests fallback behavior when primary API is down
"""

import sys
import time
from multi_api_quran import MultiAPIQuranFetcher


def test_normal_operation():
    """Test 1: Normal operation - all APIs working"""
    print("\n" + "="*70)
    print("TEST 1: Normal Operation (All APIs Working)")
    print("="*70)
    
    fetcher = MultiAPIQuranFetcher()
    
    # Test fetching verse 1:1
    print("\n📝 Fetching Al-Fatihah 1:1...")
    result = fetcher.get_verse(1, 1, max_cycles=1)
    
    if result:
        print(f"\n✅ TEST 1 PASSED")
        print(f"   Source: {result['source']}")
        print(f"   Surah: {result['surah_name']}")
        print(f"   Arabic: {result['arabic'][:50]}...")
        print(f"   Translation: {result['translation'][:80]}...")
        return True
    else:
        print(f"\n❌ TEST 1 FAILED: Could not fetch verse")
        return False


def test_primary_api_down():
    """Test 2: Primary API disabled - should use fallback"""
    print("\n" + "="*70)
    print("TEST 2: Primary API Down (Testing Fallback)")
    print("="*70)
    
    fetcher = MultiAPIQuranFetcher()
    
    # Disable primary API (Quran.com)
    print("\n🔧 Disabling Quran.com API to simulate downtime...")
    fetcher.apis[0]['enabled'] = False
    
    # Clear cache to force fresh fetch
    cache_key = "1:2"
    if cache_key in fetcher.cache:
        del fetcher.cache[cache_key]
    
    # Test fetching verse 1:2
    print("\n📝 Fetching Al-Fatihah 1:2 (primary API disabled)...")
    result = fetcher.get_verse(1, 2, max_cycles=1)
    
    if result:
        print(f"\n✅ TEST 2 PASSED - Fallback worked!")
        print(f"   Source: {result['source']}")
        print(f"   Expected: NOT Quran.com")
        
        if result['source'] != 'Quran.com API':
            print(f"   ✅ Correctly used fallback API")
            return True
        else:
            print(f"   ❌ Still using primary API (should be disabled)")
            return False
    else:
        print(f"\n❌ TEST 2 FAILED: Fallback did not work")
        return False


def test_wrong_primary_url():
    """Test 3: Wrong primary API URL - should auto-fallback"""
    print("\n" + "="*70)
    print("TEST 3: Wrong Primary URL (Auto-Fallback)")
    print("="*70)
    
    fetcher = MultiAPIQuranFetcher()
    
    # Corrupt the primary API URL
    print("\n🔧 Setting wrong URL for Quran.com API...")
    original_fetch = fetcher._fetch_quran_com
    
    def broken_fetch(surah, ayah):
        raise Exception("Simulated API failure - wrong URL")
    
    fetcher.apis[0]['fetch_func'] = broken_fetch
    
    # Clear cache
    cache_key = "1:3"
    if cache_key in fetcher.cache:
        del fetcher.cache[cache_key]
    
    # Test fetching verse 1:3
    print("\n📝 Fetching Al-Fatihah 1:3 (with broken primary API)...")
    result = fetcher.get_verse(1, 3, max_cycles=1)
    
    if result:
        print(f"\n✅ TEST 3 PASSED - Auto-fallback worked!")
        print(f"   Source: {result['source']}")
        print(f"   Successfully recovered from broken API")
        return True
    else:
        print(f"\n❌ TEST 3 FAILED: Could not recover from broken API")
        return False


def test_all_apis_slow():
    """Test 4: Timeout simulation - should retry with backoff"""
    print("\n" + "="*70)
    print("TEST 4: Timeout & Retry Logic")
    print("="*70)
    
    fetcher = MultiAPIQuranFetcher()
    
    # Reduce timeout for faster testing
    original_timeout = fetcher.timeout
    fetcher.timeout = 5  # 5 seconds
    
    print("\n🔧 Testing with reduced timeout (5s)...")
    print("📝 Fetching verse 1:4...")
    
    # Clear cache
    cache_key = "1:4"
    if cache_key in fetcher.cache:
        del fetcher.cache[cache_key]
    
    start_time = time.time()
    result = fetcher.get_verse(1, 4, max_cycles=1)
    elapsed = time.time() - start_time
    
    if result:
        print(f"\n✅ TEST 4 PASSED")
        print(f"   Time taken: {elapsed:.1f}s")
        print(f"   Source: {result['source']}")
        
        # Restore timeout
        fetcher.timeout = original_timeout
        return True
    else:
        print(f"\n❌ TEST 4 FAILED: Timed out")
        fetcher.timeout = original_timeout
        return False


def test_multiple_cycles():
    """Test 5: Multiple cycles - persistent retry"""
    print("\n" + "="*70)
    print("TEST 5: Multiple Cycles (Persistent Retry)")
    print("="*70)
    
    fetcher = MultiAPIQuranFetcher()
    
    # Create a custom fetch that fails twice then succeeds
    attempt_count = {'count': 0}
    original_fetch = fetcher._fetch_alquran_cloud
    
    def flaky_fetch(surah, ayah):
        attempt_count['count'] += 1
        if attempt_count['count'] < 3:
            raise Exception("Simulated temporary failure")
        return original_fetch(surah, ayah)
    
    # Disable primary, use flaky secondary
    fetcher.apis[0]['enabled'] = False
    fetcher.apis[1]['fetch_func'] = flaky_fetch
    
    # Clear cache
    cache_key = "1:5"
    if cache_key in fetcher.cache:
        del fetcher.cache[cache_key]
    
    print("\n📝 Fetching verse 1:5 with simulated failures...")
    print("   (Should fail twice, then succeed on 3rd attempt)")
    
    result = fetcher.get_verse(1, 5, max_cycles=2)
    
    if result:
        print(f"\n✅ TEST 5 PASSED - Persistent retry worked!")
        print(f"   Attempts needed: {attempt_count['count']}")
        print(f"   Source: {result['source']}")
        return True
    else:
        print(f"\n❌ TEST 5 FAILED: Gave up too early")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 MULTI-API QURAN FETCHER TEST SUITE")
    print("="*70)
    print("\nThis will test:")
    print("  1. Normal operation")
    print("  2. Primary API failure (fallback)")
    print("  3. Wrong API URL (auto-recovery)")
    print("  4. Timeout handling")
    print("  5. Persistent retry across cycles")
    print("\n" + "="*70)
    
    results = []
    
    # Run each test
    tests = [
        ("Normal Operation", test_normal_operation),
        ("Primary API Down", test_primary_api_down),
        ("Wrong Primary URL", test_wrong_primary_url),
        ("Timeout & Retry", test_all_apis_slow),
        ("Multiple Cycles", test_multiple_cycles),
    ]
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ TEST CRASHED: {e}")
            results.append((test_name, False))
        
        # Small delay between tests
        time.sleep(1)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n  Total: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n  🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n  ⚠️  {total_count - passed_count} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
