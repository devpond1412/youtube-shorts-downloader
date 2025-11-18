import json
import os
import time
import threading
from typing import Callable, Optional

from core import run_yt_dlp, FFMPEG_EXE


StatusCallback = Callable[[str], None]
ProgressCallback = Callable[[int, int], None]
FinishedCallback = Callable[[bool, str], None]


class Downloader:
    """Background worker that lists and downloads Shorts for a channel."""

    def __init__(
        self,
        output_dir: str,
        on_status: StatusCallback,
        on_progress: ProgressCallback,
        on_finished: FinishedCallback,
    ) -> None:
        self.output_dir = output_dir
        self.on_status = on_status
        self.on_progress = on_progress
        self.on_finished = on_finished

        self.total = 0
        self.done = 0

        self._paused = False
        self._stopped = False
        self._thread: Optional[threading.Thread] = None

    def start(self, channel_handle: str) -> None:
        """Start downloading in a separate thread."""
        if self._thread and self._thread.is_alive():
            return
        self._paused = False
        self._stopped = False
        self._thread = threading.Thread(
            target=self._run, args=(channel_handle,), daemon=True
        )
        self._thread.start()

    def pause_toggle(self) -> None:
        """Toggle paused state."""
        self._paused = not self._paused

    def stop(self) -> None:
        """Request the worker to stop."""
        self._stopped = True

    def _run(self, channel_handle: str) -> None:
        try:
            url = f"https://www.youtube.com/{channel_handle}/shorts"
            self.on_status("Fetching Shorts list...")

            stdout = run_yt_dlp(["-J", "--flat-playlist", url], capture_json=True)
            data = json.loads(stdout or "{}")
            entries = data.get("entries", []) or []

            self.total = len(entries)
            self.done = 0

            if self.total == 0:
                msg = "No Shorts found."
                self.on_status(msg)
                self.on_finished(False, msg)
                return

            self.on_status(f"Found {self.total} videos. Starting downloads...")

            for entry in entries:
                if self._stopped:
                    msg = "Download stopped by user."
                    self.on_status(msg)
                    self.on_finished(False, msg)
                    return

                while self._paused and not self._stopped:
                    time.sleep(0.2)

                video_url = entry.get("url") or entry.get("id")
                if not video_url:
                    continue

                outtmpl = os.path.join(self.output_dir, "%(title)s.%(ext)s")

                run_yt_dlp(
                    [
                        "-f",
                        "bv*+ba/best",
                        "--merge-output-format",
                        "mp4",
                        "--ffmpeg-location",
                        FFMPEG_EXE,
                        "-o",
                        outtmpl,
                        video_url,
                    ],
                    capture_json=False,
                )

                self.done += 1
                self.on_progress(self.done, self.total)

            msg = "Download completed."
            self.on_status(msg)
            self.on_finished(True, msg)

        except Exception as exc:
            msg = f"Error: {exc}"
            self.on_status(msg)
            self.on_finished(False, msg)
