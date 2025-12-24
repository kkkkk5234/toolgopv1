import cloudscraper
import json
import re
import sys
from typing import Optional

API_TOKEN = "68ee653ab963c96e472dd8c1"  # <-- đổi nếu cần
HTML_LINK = "https://kkkkk5234.github.io/toolgopv1/Index.html  # trang cần rút gọn
MK_RAW_LINK = "https://raw.githubusercontent.com/kkkkk5234/toolgopv1/main/key.json"  # đường dẫn raw của mk.json

API_ENDPOINT = "https://link4m.com/api-shorten?api={api}&url={url}"

scraper = cloudscraper.create_scraper()

def shorten(original_url: str, timeout: int = 20) -> Optional[str]:
    api_url = API_ENDPOINT.format(api=API_TOKEN, url=original_url)
    try:
        resp = scraper.get(api_url, timeout=timeout)
    except Exception as e:
        print(f"Error: request failed for {original_url}: {e}", file=sys.stderr)
        return None

    body = resp.text or ""
    # try parse JSON first
    try:
        data = json.loads(body)
        # thử nhiều khóa phổ biến
        candidate = (
            data.get("url")
            or data.get("shortenedUrl")
            or data.get("short_url")
            or data.get("result")
            or data.get("data")
            or None
        )
        if isinstance(candidate, dict):
            # có thể nested
            candidate = candidate.get("url") or candidate.get("short_url") or None
        if isinstance(candidate, str) and candidate.strip():
            return candidate.replace("\\/", "/")
    except Exception:
        pass

    # fallback: tìm bằng regex trong response text
    body_unescaped = body.replace("\\/", "/")
    match = re.search(r"https?://link4m\.com/[A-Za-z0-9_-]+", body_unescaped)
    if match:
        return match.group(0)

    # Nếu không tìm thấy
    print(f"Error: không tìm được link rút gọn trong phản hồi cho {original_url}", file=sys.stderr)
    return None

def main():
    short_html = shorten(HTML_LINK)
    if not short_html:
        sys.exit(1)

    short_mk = shorten(MK_RAW_LINK)
    if not short_mk:
        sys.exit(2)

    # In đúng định dạng yêu cầu, KHÔNG in gì thêm
    print(f"Link key 24h: {short_html}")
    print(f"Link mk để nhận key: {short_mk}")

if __name__ == "__main__":
    main()