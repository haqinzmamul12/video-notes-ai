import os
import shutil
import yt_dlp
import uuid
import constants

DATA_DIR = "data"

# === Generate unique video ID and path ===
video_id = str(uuid.uuid4())[:8]
video_dir = os.path.join(DATA_DIR, "videos")
os.makedirs(video_dir, exist_ok=True)

# Final video file path
video_path = os.path.join(video_dir, f"{video_id}.mp4")

def save_uploaded_file(uploaded_file):
    with open(video_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    return video_path


def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': video_path
    }

    video_title = "Unknown Title"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)  # ⬅️ download + get metadata
        video_title = info_dict.get('title', video_title)

    print("Video path:", video_path)
    print("Video title:", video_title)

    constants.config['video_title'] =video_title
    return video_path, video_id


    # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([url])

    # print("Video path:", video_path)
    # return video_path, video_id


# if __name__=="__main__":
#     download_youtube_video("https://youtu.be/OS9xRGKfx4E?si=Zi-VUDxsVGTQmQ8I")
