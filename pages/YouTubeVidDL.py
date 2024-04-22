import streamlit as st
from pytube import YouTube
import os
from tempfile import NamedTemporaryFile
import base64

st.title('YouTube Video Downloader')

# Function to download video and return path
def download_video(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        with NamedTemporaryFile(delete=False) as tmpfile:
            stream.download(output_path=tmpfile.name)
            tmpfile_path = f"{tmpfile.name}.mp4"
            os.rename(tmpfile.name, tmpfile_path)
            return tmpfile_path
    return None

# Function to generate download link for the video file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Initialize session state
if 'url_list' not in st.session_state:
    st.session_state.url_list = ['']

# Function to add new URL input box
def add_url_input():
    st.session_state.url_list.append('')

# Button to add new URL input box
st.button("Add another URL box", on_click=add_url_input)

# Display URL input boxes
for i in range(len(st.session_state.url_list)):
    st.session_state.url_list[i] = st.text_input(f"Enter the video URL #{i+1}", key=f"url_{i}")

# Button to download videos
if st.button('Download Videos'):
    for url in st.session_state.url_list:
        if not url:
            st.warning(f"URL #{st.session_state.url_list.index(url)+1} is empty. Please enter a URL or remove the box.")
            continue
        video_path = download_video(url)
        if video_path:
            # Display a link that will download the video to the local machine
            st.markdown(get_binary_file_downloader_html(video_path, 'Video'), unsafe_allow_html=True)
            # Clean up the file after serving it to the client
            os.unlink(video_path)
        else:
            st.error(f'An error occurred during downloading video from URL #{st.session_state.url_list.index(url)+1}. Please check the URL and try again.')
