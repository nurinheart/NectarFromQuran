import requests

# Try community wrapper
url = 'https://quranapi.pages.dev/api/tafsir/2_255.json'  # surah 2 ayah 255
print(f'Fetching from: {url}')
r = requests.get(url, timeout=10)
print(f'Status: {r.status_code}')

if r.status_code == 200:
    resp = r.json()
    print(f'Keys: {list(resp.keys())}')
    
    if 'tafsirs' in resp:
        print(f'Tafsirs count: {len(resp["tafsirs"])}')
        # Find Ibn Kathir
        ibn = next((t for t in resp['tafsirs'] if 'Ibn Kathir' in t.get('author', '')), None)
        if ibn:
            print(f"\nFound Ibn Kathir!")
            print(f"Author: {ibn['author']}")
            print(f"Content (500 chars):\n{ibn['content'][:500]}...")
        else:
            print(f'\nAvailable authors:')
            for t in resp['tafsirs'][:5]:
                print(f"  - {t.get('author', 'Unknown')}")
