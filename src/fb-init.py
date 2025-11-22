from yt_dlp import YoutubeDL
import subprocess
import os

url = "https://web.facebook.com/reel/1497458021524786/?rdid=sW3Ya5FNuxD5g0q5&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2Fr%2F1FE4Vx4SbH%2F&_rdc=1&_rdr"

ydl_opts = {
    "outtmpl": "downloaded.%(ext)s",   
    "format": "mp4/best"               
}

print("Downloading video...")
with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

input_file = None
for ext in ["mp4", "mkv", "webm"]:
    f = f"downloaded.{ext}"
    if os.path.exists(f):
        input_file = f
        break

if not input_file:
    raise Exception("Error: ไม่เจอไฟล์วิดีโอที่โหลดมา")

output_file = "output_9x16.mp4"

print("Converting to 9:16...")
cmd = [
    "ffmpeg",
    "-i", input_file,
    "-vf", "crop=in_h*9/16:in_h,scale=1080:1920",
    "-c:a", "copy",
    output_file
]

subprocess.run(cmd)

print("Done!")
print("Saved video as:", output_file)
