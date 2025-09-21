import shutil

def clean_temp_files(file):
    dirs = ["data/audios", "data/videos", "data/frames"]
    for d in dirs:
        if file in d:
            shutil.rmtree(d, ignore_errors=True)
            print(f"The Directory: {d} deleted successfully")
