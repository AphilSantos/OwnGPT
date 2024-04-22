import streamlit as st
from pytube import YouTube
import os

st.title('Video Downloader')

# Input field for the video URL
url = st.text_input('Enter the video URL from YouTube')

# Function to download the video
def download_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        stream.download()
        return True
    return False

# Download button
if st.button('Download Video'):
    if not url:
        st.warning('Please enter a URL')
    else:
        success = download_video(url)
        if success:
            st.success('Downloaded video successfully!')
        else:
            st.error('An error occurred during downloading.')

