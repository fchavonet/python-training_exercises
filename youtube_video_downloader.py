#!/usr/bin/env python3

import sys
import shutil
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# ANSI escape codes for colored output.
BLUE = "\033[94m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
RED = "\033[91m"
YELLOW = "\033[93m"

RESET = "\033[0m"

# Terminal width for dynamic progress bar.
terminal_width = shutil.get_terminal_size().columns
bar_width = min(50, terminal_width - 30)


class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def progress_bar(d):
    """
    Display a custom progress bar during video download.

    Args:
        d (dict): progress information provided by yt-dlp.
    """

    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
        downloaded = d.get("downloaded_bytes", 0)
        percent = downloaded / total
        filled_length = int(percent * bar_width)
        bar = f"{MAGENTA}{"=" * filled_length}{RESET}{" " * (bar_width - filled_length)}"
        sys.stdout.write(f"\r[{bar}] {percent * 100:6.2f}% ")
        sys.stdout.flush()


def download_video(video_url):
    """
    Download the highest resolution of a YouTube video.

    Args:
        video_url (str): the URL of the YouTube video to download.
    """

    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "%(uploader)s - %(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "logger": SilentLogger(),
            "progress_hooks": [progress_bar],
            "no_warnings": True,
            "quiet": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print(f"\n{GREEN}Download complete.{RESET}\n")

    except DownloadError:
        print(f"{RED}ERROR: Could not download video.{RESET}\n")


def main():
    """
    Main function to prompt the user for a YouTube video URL and download it.
    """
    print(f"\n{YELLOW}YOUTUBE VIDEO DOWNLOADER")
    print("=" * 24)

    video_url = input(f"\n{RESET}Enter the YouTube video URL to download: ")
    download_video(video_url)


if __name__ == "__main__":
    main()
