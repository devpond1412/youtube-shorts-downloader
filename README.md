# youtube-shorts-downloader

A tiny desktop tool for bulk-downloading all YouTube Shorts from a channel.
<div align="center">
  <img width="256" alt="icon" src="https://github.com/user-attachments/assets/a4d69d8a-cafe-4bdd-8e26-717dfdb81ec6" />
</div>
> Built for my own workflow, but you’re welcome to use or fork it.

## Tutorial images
<div align="center">
  <img width="310" src="https://github.com/user-attachments/assets/678f33a7-d7a7-4244-b840-58a8babc1dd0" />
  <img width="314" src="https://github.com/user-attachments/assets/0e35c21f-576e-475b-a76a-a7d19d3f2b74" />
  <img width="321" src="https://github.com/user-attachments/assets/45efd485-6d3a-4acd-8950-9386f18378b5" />
  <img width="321" src="https://github.com/user-attachments/assets/0480ecf2-386d-416e-93be-42f1c78a47d5" />
</div>

## Ingredients
- Python and [pip](https://pypi.org/project/pip/)
    - [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl with additional features  
    - [Tkinter](https://docs.python.org/3/library/tkinter.html) - for building, good-quality for windowapps
    - [PyInstaller](https://pyinstaller.org/en/stable/) - bundles everything into a single windows  executable
- [ffmpeg](https://www.ffmpeg.org/) - merges video + audio into MP4
    

## How to use
1. Paste a channel handle like @PewDiePie
2. Choose an output folder
3. Start the download

## debug & build
```bash
pip install -r requirements.txt
py src/main.py
```
### Building a Windows EXE From the project root

```bash
pyinstaller --noconsole --onefile --icon=icon.ico ^
  --add-binary "ffmpeg.exe;." ^
  --add-binary "yt-dlp.exe;." ^
  src\main.py
```
    
## Project Structure
```bash
PROJECT_ROOT
├─ src/
│  ├─ core.py        # paths, yt-dlp wrapper, shared helpers
│  ├─ downloader.py  # download logic (no UI)
│  ├─ ui.py          # Tkinter GUI
│  └─ main.py        # entrypoint
├─ shorts/           # optional: where you keep downloaded videos
├─ yt-dlp.exe
├─ ffmpeg.exe
├─ icon.ico
└─ README.md
```

## License
MIT License.

