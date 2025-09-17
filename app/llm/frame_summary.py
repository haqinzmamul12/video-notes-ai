from langchain_groq import ChatGroq 
import base64
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image
import os
import imagehash
from dotenv import load_dotenv 
import constants
import glob

# Constants
DATA_DIR ="data"
SUMMARY_DIR = os.path.join(DATA_DIR, "summaries")



 


#title = "This video is all about Anomaly detection Technique in Machine Learning."
video_title = constants.config['video_title']
PROMPT = (
    f"You are an AI assistant analyzing image frames from a video titled: '{video_title}'.\n\n"
    "Your job is to extract **only information that is directly related** to the video's topic.\n\n"
    "Strictly follow these instructions:\n"
    "1. If the image contains readable, meaningful content related to Artificial Intelligence (such as definitions, diagrams, or technical descriptions), summarize it in 1–2 clear, factual sentences.\n"
    "2. Do NOT describe browser windows, tabs, unreadable text, layouts, or logos.\n"
    "3. If the frame contains no readable or relevant information about AI, respond only with: '.'\n"
    "4. Avoid filler phrases like 'This image shows...' or 'The image contains...'. Focus only on content.\n\n"
    "Return your response as a single sentence or 'No relevant content in this frame.'"
)



load_dotenv() 
GROQ_API_KEY =os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] =GROQ_API_KEY
VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"


def save_file(summaries, video_id):
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    SUMMARY_PATH =os.path.join(SUMMARY_DIR, f"{video_id}.txt") 
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        for i, summary in enumerate(summaries):
            f.write(f"Summary {i+1}:\n{summary}\n\n")

    print(f"Summaries are saved at {SUMMARY_PATH}")
    return SUMMARY_PATH


def get_image_hash(image_path: str) -> str:
    """Generate a perceptual hash of the image."""
    try:
        with Image.open(image_path) as img:
            return str(imagehash.phash(img))
    except Exception as e:
        print(f"Error hashing image {image_path}: {e}")
        return None

def is_duplicate(current_hash: str, previous_hash: str, threshold: int = 5) -> bool:
    """Check if current image is visually similar to the previous one."""
    if current_hash is None or previous_hash is None:
        return False
    return imagehash.hex_to_hash(current_hash) - imagehash.hex_to_hash(previous_hash) <= threshold


def encode_image(image_path):
    """Encodes an image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_summary(image_path):
    """Generates a summary for the given image."""
    # Encode the image
    base64_image = encode_image(image_path)

    human_msg = HumanMessage(content=[
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
    ])
    
    # Instantiate the model
    chat = ChatGroq(
        model_name= VISION_MODEL,
        temperature=0.7,
        max_tokens=512,  # adjust as needed
        groq_api_key=GROQ_API_KEY
    )

    response = chat.invoke([human_msg])
    return response.content


def frame_summary_extractor(video_id):
    # List of image paths
    image_paths = glob.glob(f"data/frames/{video_id}/*.jpg")
    
    summaries = []
    previous_hash =None 
    i =1
    for image_path in image_paths:
        if os.path.exists(image_path):
            current_hash = get_image_hash(image_path)

            if is_duplicate(current_hash, previous_hash):
                print(f"⏭️ Skipped duplicate frame: {image_path}")
                continue

            summary = generate_summary(image_path)
            previous_hash = current_hash
            summaries.append(f"Response-{i}: {summary}")
            i +=1 
        else:
            print(f"Image {image_path} not found.")

    
    save_file(summaries, video_id)

# if __name__=="__main__":
#     frame_summary_extractor("edff92fe")
    

