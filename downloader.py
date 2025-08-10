import streamlit as st
import yt_dlp
import os

# Create downloads folder
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def sanitize_url(url: str) -> str:
    """Convert Shorts URL to normal watch URL if needed."""
    if "shorts/" in url:
        video_id = url.split("shorts/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def download_video(url, fmt):
    url = sanitize_url(url)
    
    # yt-dlp options
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "merge_output_format": fmt,
        "format": "bestvideo+bestaudio/best" if fmt == "mp4" else "bestaudio/best",
        "quiet": True,
        "noprogress": True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Rename if merge_output_format changed extension
            if not filename.endswith(fmt):
                base = os.path.splitext(filename)[0]
                filename = f"{base}.{fmt}"
            return filename
    except Exception as e:
        st.error(f"Download failed: {e}")
        return None

# Streamlit UI
st.title("📥 YouTube Video / Audio Downloader")

video_url = st.text_input("Enter YouTube Video or Shorts URL")
format_choice = st.radio("Select format:", ["mp4", "mp3"])
if st.button("Download"):
    if not video_url.strip():
        st.warning("Please enter a valid YouTube URL")
    else:
        with st.spinner("Downloading... Please wait"):
            file_path = download_video(video_url.strip(), format_choice)
        
        if file_path and os.path.exists(file_path):
            st.success("✅ Download completed!")
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇ Download File",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4" if format_choice == "mp4" else "audio/mpeg"
                )
