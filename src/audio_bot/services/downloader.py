from pathlib import Path
from typing import Any

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class AudioDownloader:
    def __init__(self, download_dir: Path | str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def extract_metadata(self, url: str) -> dict[str, Any]:
        opts = {
            "extract_flat": False,
            "quiet": True,
            "noplaylist": True,
        }

        with YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
            info = ydl.extract_info(url, download=False)

            if not info:
                raise DownloadError("Cant get video metadata")

            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
            }

    def download_audio(self, url: str) -> Path:
        output_template = str(self.download_dir / "%(id)s.%(ext)s")
        opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                }
            ],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }

        with YoutubeDL(opts) as ydl:  # type: ignore[arg-type]
            info = ydl.extract_info(url, download=True)
            if not info:
                raise DownloadError("Video download error")

            video_id = info.get("id")
            result_path = self.download_dir / f"{video_id}.m4a"
            return result_path
