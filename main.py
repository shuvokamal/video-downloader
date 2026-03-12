import argparse
import sys
from video_downloader.core.downloader import download

def main():
    parser = argparse.ArgumentParser(description="Download public videos from YouTube, Facebook, and Twitter/X")
    parser.add_argument("url", help="Public video URL to download")
    parser.add_argument("--output", default="downloads", help="Output directory (default: downloads)")
    args = parser.parse_args()

    try:
        download(args.url, args.output)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
