# youtube_downloader_app.py
import streamlit as st
import yt_dlp
import os

st.title("🎬 YouTube Video/Audio Downloader")
st.write("Paste a YouTube link below and choose your format.")

# Input fields
url = st.text_input("Enter YouTube URL")
format_choice = st.selectbox("Select format", ["MP4 (Video)", "MP3 (Audio)"])

# Temporary download directory
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url, format_choice):
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
    }
    
    if "MP3" in format_choice:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({"format": "bestvideo+bestaudio"})

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Get last downloaded file
    latest_file = sorted(os.listdir(DOWNLOAD_DIR), key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)))[-1]
    return os.path.join(DOWNLOAD_DIR, latest_file)

if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            try:
                file_path = download_video(url, format_choice)
                st.success("Download complete!")
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Click to Download",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4" if "MP4" in format_choice else "audio/mpeg"
                    )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
