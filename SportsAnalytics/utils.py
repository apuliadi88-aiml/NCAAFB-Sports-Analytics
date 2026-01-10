import time
import requests

def api_get(url, headers, max_retries=5, timeout=15):
    """GET request with retries and exponential backoff."""
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            wait = min(2 ** attempt, 60)
            print(f"429 received. Sleeping {wait}s...")
            time.sleep(wait)
        elif response.status_code == 404:
            print(f"Resource not found: {url}")
            return None
        else:
            print(f"Error {response.status_code} for {url}")
            return None
    print(f"Max retries exceeded for {url}")
    return None
