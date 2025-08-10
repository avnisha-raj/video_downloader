import os
import streamlit as st
import yt_dlp

def download_video(url, file_format):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if file_format == "mp4" else 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': file_format,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        if file_format == "mp3":
            base, _ = os.path.splitext(filename)
            filename = base + ".mp3"

        return filename

# Streamlit UI
st.title(" YouTube Downloader")
link = st.text_input("Enter YouTube Video URL")
format_choice = st.selectbox("Select format", ["mp4", "mp3"])

if st.button("Download"):
    if link:
        filepath = download_video(link, format_choice)
        with open(filepath, "rb") as f:
            st.download_button(
                label=" Click to Download",
                data=f,
                file_name=os.path.basename(filepath),
                mime="video/mp4" if format_choice == "mp4" else "audio/mpeg"
            )
    else:
        st.error("Please enter a valid URL")
