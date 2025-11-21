"""
Check if Ibn Kathir tafsir has sections/summary
and compare with other available tafsirs
"""

import requests
import json

# Test with Ayat al-Kursi (2:255)
url = "https://quranapi.pages.dev/api/tafsir/2_255.json"
response = requests.get(url)
data = response.json()

print("=" * 80)
print("AVAILABLE TAFSIRS FOR AYAH 2:255")
print("=" * 80)

for idx, tafsir in enumerate(data['tafsirs'], 1):
    author = tafsir.get('author', 'Unknown')
    content = tafsir.get('content', '')
    
    print(f"\n{idx}. {author}")
    print(f"   Length: {len(content):,} characters")
    
    # Check for sections (##, headings, etc.)
    has_markdown_headers = '##' in content
    has_html = '<' in content and '>' in content
    line_count = content.count('\n')
    
    print(f"   Has sections/headers: {has_markdown_headers}")
    print(f"   Has HTML: {has_html}")
    print(f"   Paragraph breaks: {line_count}")
    
    # Show first 300 chars
    print(f"\n   Preview (first 300 chars):")
    print(f"   {content[:300]}")
    print(f"   ...")

# Now check specifically for Tazkirul Quran
print("\n" + "=" * 80)
print("CHECKING FOR TAZKIRUL QURAN")
print("=" * 80)

tazkirul = next((t for t in data['tafsirs'] if 'Tazkirul' in t.get('author', '') or 'Maududi' in t.get('author', '')), None)

if tazkirul:
    print(f"\n✅ Found: {tazkirul['author']}")
    print(f"   Length: {len(tazkirul['content']):,} characters")
    print(f"\n   Full content:")
    print(f"   {tazkirul['content'][:1000]}")
else:
    print("\n❌ Tazkirul Quran not found in this API")
    print("\nAvailable authors:")
    for t in data['tafsirs']:
        print(f"   - {t.get('author', 'Unknown')}")
