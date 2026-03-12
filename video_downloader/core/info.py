import yt_dlp
from video_downloader.utils.helpers import detect_platform


def get_formats(url: str):
    platform = detect_platform(url)

    if platform == "youtube":
        return _youtube_formats(url)
    else:
        return _generic_formats(url, platform)


def _youtube_formats(url: str):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 10,
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = info.get("formats", [])
    title = info.get("title", "video")

    # Get 360p combined stream for direct download
    direct_360 = None
    audio_size = 0
    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") != "none" and f.get("height") == 360 and f.get("url"):
            size = f.get("filesize") or f.get("filesize_approx") or 0
            direct_360 = {"url": f["url"], "size": size}
        if f.get("vcodec") == "none" and f.get("acodec") != "none":
            size = f.get("filesize") or f.get("filesize_approx") or 0
            if size > audio_size:
                audio_size = size

    results = []

    if direct_360:
        results.append({
            "height": 360,
            "label": "360p MP4",
            "size_mb": round(direct_360["size"] / (1024 * 1024), 1) if direct_360["size"] else None,
            "download_type": "direct",
            "direct_url": direct_360["url"],
        })
    else:
        raise ValueError("No downloadable format found for this video.")

    return results, title


def _generic_formats(url: str, platform: str):
    """For Facebook, Twitter/X — combined streams, no merging needed."""
    opts = {
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 10,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = info.get("formats", [])
    title = info.get("title", "video")

    # Facebook/Twitter serve combined streams — just pick by height
    seen = set()
    results = []

    for f in sorted(formats, key=lambda x: x.get("height") or 0, reverse=True):
        height = f.get("height")
        vcodec = f.get("vcodec", "none")
        acodec = f.get("acodec", "none")
        ext = f.get("ext", "")

        if not height or vcodec == "none":
            continue
        if height in seen:
            continue

        seen.add(height)
        is_combined = acodec != "none"
        size = f.get("filesize") or f.get("filesize_approx") or 0

        entry = {
            "height": height,
            "label": f"{height}p MP4",
            "size_mb": round(size / (1024 * 1024), 1) if size else None,
        }

        if is_combined and f.get("url"):
            entry["download_type"] = "direct"
            entry["direct_url"] = f["url"]
        else:
            entry["download_type"] = "server"
            entry["format_id"] = f"best[height<={height}][ext=mp4]/best[height<={height}]/best"

        results.append(entry)

    results.sort(key=lambda x: x["height"])

    # MP3 option
    results.append({
        "height": 0,
        "label": "MP3 Audio",
        "size_mb": None,
        "download_type": "server",
        "format_id": "mp3",
    })

    return results, title
