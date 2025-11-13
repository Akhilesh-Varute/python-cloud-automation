# client_post.py
import time
import requests
import json
from requests.exceptions import RequestException, HTTPError

ENDPOINTS = [
    "https://httpbin.org/post",  # original (may be flaky)
    "https://postman-echo.com/post",  # reliable echo service
    "https://reqres.in/api/users",  # simple test API (creates resource)
    "http://127.0.0.1:8000/transform",  # your local FastAPI (if running)
]

PAYLOAD = {"name": "akhil", "score": 44}
HEADERS = {"Content-Type": "application/json", "User-Agent": "python-client/1.0"}


def try_post_with_retries(url, payload, headers, max_retries=3, backoff=1.0):
    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            # raise for 4xx/5xx so we can handle them
            resp.raise_for_status()
            return resp
        except HTTPError as he:
            status = None
            try:
                status = he.response.status_code
            except Exception:
                pass
            # Retry on 5xx server errors; fail fast on 4xx
            if status and 500 <= status < 600:
                print(
                    f"[{url}] Server error {status} (attempt {attempt}/{max_retries}). Retrying after {backoff}s..."
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            else:
                # 4xx or no status — don't retry
                print(f"[{url}] HTTP error: {he}. Not retrying.")
                raise
        except RequestException as e:
            # network / TLS / connection problems — retry a few times
            print(
                f"[{url}] Network/TLS error (attempt {attempt}/{max_retries}): {e}. Retrying after {backoff}s..."
            )
            time.sleep(backoff)
            backoff *= 2
            continue
    raise RuntimeError(f"Failed to POST to {url} after {max_retries} attempts")


def main():
    for url in ENDPOINTS:
        print("\nTrying:", url)
        try:
            resp = try_post_with_retries(
                url, PAYLOAD, HEADERS, max_retries=3, backoff=1
            )
            print("Success ->", resp.status_code)
            # safe attempt to show JSON (some endpoints wrap/rename)
            try:
                data = resp.json()
                print("Response JSON (preview):")
                print(json.dumps(data, indent=2)[:1000])
            except Exception:
                print("Response text (preview):")
                print(resp.text[:1000])
            return
        except Exception as e:
            print(f"Failed on {url}: {e}")
            # try next endpoint
    print(
        "\nAll endpoints failed. If you want a guaranteed test, run your local FastAPI server:"
    )
    print("1) In another terminal: uvicorn api_transform:app --reload --port 8000")
    print("2) Then re-run this script (it will try http://127.0.0.1:8000/transform).")


if __name__ == "__main__":
    main()
