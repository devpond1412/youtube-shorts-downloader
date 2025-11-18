import os
import sys
import subprocess
from typing import Optional, List


def resource_path(name: str) -> str:
    """Return absolute path for a resource in dev and bundled modes."""
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


YTDLP_EXE = resource_path("yt-dlp.exe")
FFMPEG_EXE = resource_path("ffmpeg.exe")


def run_yt_dlp(args: List[str], capture_json: bool = False) -> Optional[str]:
    """Run yt-dlp.exe without opening a console window."""
    creationflags = 0
    if os.name == "nt" and hasattr(subprocess, "CREATE_NO_WINDOW"):
        creationflags = subprocess.CREATE_NO_WINDOW

    cmd = [YTDLP_EXE, *args]

    if capture_json:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
            creationflags=creationflags,
        )
        return proc.stdout
    else:
        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            creationflags=creationflags,
        )
        return None
