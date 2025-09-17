import os 
import cv2 


DATA_DIR ="data"

def extract_frames(video_id, frame_rate =2):
  try:
    frame_output_dir = os.path.join(DATA_DIR, "frames", video_id)
    os.makedirs(frame_output_dir, exist_ok=True)
    print(f"Frames directory created at: {frame_output_dir}")
    video_path =f"data/videos/{video_id}.mp4"
    cap =cv2.VideoCapture(video_path)
    fps =cap.get(cv2.CAP_PROP_FPS)
    count =0
    success, image =cap.read()
    while success:
      if int(cap.get(1)) % int(fps * frame_rate)==0:
        frame_path =os.path.join(frame_output_dir, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, image)
        count +=1

      success, image =cap.read()
    cap.release()

  except Exception as e:
    print(f"Error ar generating frames: {repr(e)}")

