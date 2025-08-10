
!pip install -U yt-dlp
!apt install ffmpeg -y

import os
import zipfile

download_path = "/content/YouTubeDownloads"
os.makedirs(download_path, exist_ok=True)

link = input("Enter YouTube video or playlist URL: ").strip()
file_format = input("Enter format (mp4/mp3): ").strip().lower()

if file_format == "mp3":
    ytdlp_cmd = f'yt-dlp -x --audio-format mp3 --ffmpeg-location /usr/bin --fragment-retries 10 --no-abort-on-error -o "{download_path}/%(title)s.%(ext)s" "{link}"'
else:
    # Limit resolution to 720p for faster downloads in Colab
    ytdlp_cmd = f'yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" --merge-output-format mp4 --ffmpeg-location /usr/bin --fragment-retries 10 --no-abort-on-error -o "{download_path}/%(title)s.%(ext)s" "{link}"'

os.system(ytdlp_cmd)

# Zip results
zip_file = "/content/YouTubeDownloads.zip"
with zipfile.ZipFile(zip_file, 'w') as zipf:
    for root, dirs, files in os.walk(download_path):
        for file in files:
            zipf.write(os.path.join(root, file), file)

print("\n Download complete & merged successfully!")
print(f" Folder: {download_path}")
print(f" ZIP: {zip_file}")
print("➡ In Colab's left panel, right-click the ZIP and choose 'Download'.")
