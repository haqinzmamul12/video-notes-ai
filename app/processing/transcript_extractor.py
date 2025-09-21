import os
#import whisper
from faster_whisper import WhisperModel
#from moviepy import VideoFileClip  
import subprocess
import warnings
warnings.filterwarnings("ignore")

DATA_DIR ="data"
transcript_dir = os.path.join(DATA_DIR, "transcripts")




def save_file(transcript, video_id):
    try:
        os.makedirs(transcript_dir, exist_ok=True)
        transcript_path = os.path.join(transcript_dir, f"{video_id}.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Transcripts are saved at {transcript_path}")
        return transcript_path
    except Exception as e:
       print(e)

# def video_to_audio(video_id):
#     audio_dir =f"data/audios"
#     os.makedirs(audio_dir, exist_ok= True)
#     audio_path =f"{audio_dir}/{video_id}.mp3"
#     video_path =f"data/videos/{video_id}.mp4"
#     video_clip = VideoFileClip(video_path)
#     video_clip.audio.write_audiofile(audio_path)
#     return audio_path




def video_to_audio(video_id):
    audio_dir = "data/audios"
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = f"{audio_dir}/{video_id}.mp3"
    video_path = f"data/videos/{video_id}.mp4"

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # no video
        "-acodec", "libmp3lame",
        "-y",  # overwrite
        audio_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path




def extract_transcript(video_id, model_size="base"):
    print("Generating audio file...")
    audio_path = video_to_audio(video_id)
    print("Audio file is generated..")
    #model = whisper.load_model(model_size)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path, beam_size=5)

    transcript = " ".join([seg.text for seg in segments])
    return save_file(transcript, video_id)


    # print("Creating transcripts...")

    # result = model.transcribe(
    # audio_path,
    # compression_ratio_threshold=2.4,
    # logprob_threshold=-1.0,
    # no_speech_threshold=0.5
    # )
    
    # transcript = ""
    # for segment in result["segments"]:
    #   if segment["no_speech_prob"] < 0.5:
    #     transcript += segment["text"] + " "
    
    # transcript_path =save_file(transcript, video_id)
    # print("Transcript created.")
    # return transcript_path

# if __name__=='__main__':
#    extract_transcript("b6ac7afd")

   


