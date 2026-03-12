import yt_dlp


def _progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?").strip()
        eta = d.get("_eta_str", "?").strip()
        print(f"\r  Downloading: {percent} at {speed}, ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print(f"\n  Done. Processing file...")


class YouTubeDownloader:
    def __init__(self, output_dir: str = "downloads", format_id: str = None):
        self.output_dir = output_dir
        self.format_id = format_id

    def download(self, url: str):
        if self.format_id == "mp3":
            opts = {
                "outtmpl": f"{self.output_dir}/%(title)s.%(ext)s",
                "format": "bestaudio/best",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                "progress_hooks": [_progress_hook],
                "extractor_args": {"youtube": {"player_client": ["ios", "android", "tv_embedded"]}},
            }
        else:
            fmt = f"{self.format_id}" if self.format_id else "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best"
            opts = {
                "outtmpl": f"{self.output_dir}/%(title)s.%(ext)s",
                "format": fmt,
                "merge_output_format": "mp4",
                "progress_hooks": [_progress_hook],
                "extractor_args": {"youtube": {"player_client": ["ios", "android", "tv_embedded"]}},
            }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
