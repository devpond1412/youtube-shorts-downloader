import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

from core import resource_path, YTDLP_EXE, FFMPEG_EXE
from downloader import Downloader


class DownloaderApp:
    """Tkinter UI that wraps the Downloader worker."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("YT-Shorts DL")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        tk.Label(root, text="Channel handle (e.g. @PewDiePie):").pack(
            anchor="w", padx=10, pady=(10, 0)
        )

        self.channel_entry = tk.Entry(root, width=45)
        self.channel_entry.pack(padx=10)

        tk.Label(root, text="Output folder:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.path_label = tk.Label(root, text="Not selected", fg="gray")
        self.path_label.pack(anchor="w", padx=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Browse...", command=self.select_folder).pack(
            side="left", padx=5
        )

        self.start_button = tk.Button(
            button_frame, text="Start", command=self.start_download
        )
        self.start_button.pack(side="left", padx=5)

        self.pause_button = tk.Button(
            button_frame, text="Pause", state="disabled", command=self.toggle_pause
        )
        self.pause_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(
            button_frame, text="Stop", state="disabled", command=self.stop_download
        )
        self.stop_button.pack(side="left", padx=5)

        self.status_label = tk.Label(root, text="Idle", fg="#0078ff")
        self.status_label.pack(pady=8)

        self.spinner_label = tk.Label(root, text="", font=("Arial", 22))
        self.spinner_label.pack()

        self.spinner_frames = ["◐", "◓", "◑", "◒"]
        self.spinner_index = 0
        self.spinner_running = False

        self.output_dir: Optional[str] = None
        self.downloader: Optional[Downloader] = None
        self.is_running = False
        self.is_paused = False

        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

    def select_folder(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path
            self.path_label.config(text=path, fg="black")

    def start_download(self) -> None:
        if self.is_running:
            messagebox.showinfo("Info", "Download is already running.")
            return

        channel = self.channel_entry.get().strip()
        if not channel.startswith("@"):
            messagebox.showerror("Error", "Please enter a channel handle like @name.")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        if not os.path.exists(YTDLP_EXE):
            messagebox.showerror("Error", "yt-dlp.exe not found.")
            return

        if not os.path.exists(FFMPEG_EXE):
            messagebox.showerror("Error", "ffmpeg.exe not found.")
            return

        self.is_running = True
        self.is_paused = False

        self.pause_button.config(state="normal", text="Pause")
        self.stop_button.config(state="normal")
        self.spinner_running = True
        self._update_spinner()

        self.downloader = Downloader(
            output_dir=self.output_dir,
            on_status=self._callback_status,
            on_progress=self._callback_progress,
            on_finished=self._callback_finished,
        )
        self.downloader.start(channel)

    def toggle_pause(self) -> None:
        if not self.downloader:
            return
        self.downloader.pause_toggle()
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.spinner_running = False
            self.spinner_label.config(text="")
            self._set_status("Paused")
        else:
            self.pause_button.config(text="Pause")
            self.spinner_running = True
            self._update_spinner()

    def stop_download(self) -> None:
        if not self.downloader:
            return
        self.downloader.stop()
        self.spinner_running = False
        self.spinner_label.config(text="")
        self._set_status("Stopping...")

    def _set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    def _set_progress(self, done: int, total: int) -> None:
        if total <= 0:
            self.status_label.config(text="Progress: 0% (0/0)")
            return
        pct = int(done * 100 / total)
        self.status_label.config(text=f"Progress: {pct}% ({done}/{total})")

    def _callback_status(self, text: str) -> None:
        self.root.after(0, lambda: self._set_status(text))

    def _callback_progress(self, done: int, total: int) -> None:
        self.root.after(0, lambda: self._set_progress(done, total))

    def _callback_finished(self, success: bool, message: str) -> None:
        def finish_ui() -> None:
            self.is_running = False
            self.spinner_running = False
            self.spinner_label.config(text="")
            self.pause_button.config(state="disabled", text="Pause")
            self.stop_button.config(state="disabled")
            self._set_status(message)

        self.root.after(0, finish_ui)

    def _update_spinner(self) -> None:
        if self.spinner_running:
            self.spinner_label.config(text=self.spinner_frames[self.spinner_index])
            self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
            self.root.after(120, self._update_spinner)
