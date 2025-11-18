import tkinter as tk
import os
from ui import DownloaderApp
from core import resource_path

def main() -> None:
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
    # I set window icon while debigging
    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print("Failed to set icon:", e)

    app = DownloaderApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
