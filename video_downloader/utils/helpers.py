from urllib.parse import urlparse


def validate_url(url: str):
    if not url or not url.strip():
        raise ValueError("URL cannot be empty.")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Invalid URL: '{url}'. Must be a valid http/https URL.")


def detect_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    return "unknown"
