import yt_dlp


def _progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?").strip()
        eta = d.get("_eta_str", "?").strip()
        print(f"\r  Downloading: {percent} at {speed}, ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print(f"\n  Done. Processing file...")


class FacebookDownloader:
    def __init__(self, output_dir: str = "downloads", format_id: str = None):
        self.output_dir = output_dir
        self.format_id = format_id

    def download(self, url: str):
        # Facebook serves combined streams — no merging needed
        fmt = self.format_id if self.format_id else "best[ext=mp4]/best"
        opts = {
            "outtmpl": f"{self.output_dir}/%(title)s.%(ext)s",
            "format": fmt,
            "progress_hooks": [_progress_hook],
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
