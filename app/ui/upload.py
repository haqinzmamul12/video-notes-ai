import streamlit as st
import os 
import shutil 


DATA_FOLDER = "data"
def clear_data_folder():
    if os.path.exists(DATA_FOLDER):
        shutil.rmtree(DATA_FOLDER)  # Deletes the whole folder
    os.makedirs(DATA_FOLDER)        # Recreates the empty folder

def video_input():
    st.title("🎥 Video Notes AI")

    st.markdown("#### Upload a video file or paste a YouTube URL")

    # Option 1: YouTube URL
    youtube_url = st.text_input("📺 Enter YouTube URL")
    # Option 2: Upload local video
    uploaded_file = st.file_uploader("📁 Or upload a video file", type=["mp4", "mov", "avi", "mkv"])

    # Submit button
    submitted = st.button("🚀 Click here to Process")

    # Return user choice
    if submitted:
        clear_data_folder()
        if youtube_url:
            return {"type": "youtube", "data": youtube_url}
        elif uploaded_file:
            return {"type": "file", "data": uploaded_file}
        else:
            st.warning("Please provide a YouTube URL or upload a video file.")
            return None
    return None
