import os
import yt_dlp
from video_downloader.platforms.youtube import YouTubeDownloader
from video_downloader.platforms.facebook import FacebookDownloader
from video_downloader.platforms.twitter import TwitterDownloader
from video_downloader.utils.helpers import detect_platform, validate_url


def download(url: str, output_dir: str = "downloads", format_id: str = None):
    validate_url(url)
    os.makedirs(output_dir, exist_ok=True)

    platform = detect_platform(url)

    if platform == "youtube":
        downloader = YouTubeDownloader(output_dir, format_id=format_id)
    elif platform == "facebook":
        downloader = FacebookDownloader(output_dir, format_id=format_id)
    elif platform == "twitter":
        downloader = TwitterDownloader(output_dir, format_id=format_id)
    else:
        raise ValueError(f"Unsupported platform. Only YouTube, Facebook, and Twitter/X are supported.")

    try:
        downloader.download(url)
    except yt_dlp.utils.DownloadError as e:
        raise RuntimeError(f"Could not download video: {e}")
