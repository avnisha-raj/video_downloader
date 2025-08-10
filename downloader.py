import streamlit as st
import yt_dlp
import os

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url, format_choice):
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "ignoreerrors": True
    }

    if format_choice == "MP4":
        # Let yt-dlp choose best available formats automatically
        ydl_opts.update({
            "format": "bv*+ba/b",
            "merge_output_format": "mp4"
        })
    elif format_choice == "MP3":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

st.title(" YouTube Downloader (No Format Errors)")

url = st.text_input("Enter YouTube video or playlist URL:")
format_choice = st.radio("Choose format:", ["MP4", "MP3"])

if st.button("Download"):
    if url.strip():
        try:
            download_video(url, format_choice)
            st.success(" Download completed! Check 'downloads' folder.")
        except Exception as e:
            st.error(f" Error: {e}")
    else:
        st.error("Please enter a valid URL.")
