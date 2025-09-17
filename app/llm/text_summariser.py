import os
import math
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv 

load_dotenv() 
GROQ_API_KEY =os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] =GROQ_API_KEY

# === Paths ===
FINAL_NOTES_DIR = "data/final_notes"


# === Constants ===
MODEL_NAME = "llama-3.3-70b-versatile"
CHUNK_SIZE = 2000  
CHUNK_OVERLAP = 200
OUTPUT_TOKEN_LIMIT = 2048

# === Prompts ===
SYSTEM_PROMPT = """You are a helpful and professional assistant.
Your task is to extract key information and create short, concise notes in clean Markdown format from the input provided.
Focus on clear explanations, structured bullet points, and include visual context if available."""

FINAL_SUMMARY_PROMPT = """You are a note-making assistant.
You are given summaries of parts of a video (transcript and frames).
Combine them into clean, structured, final study notes in Markdown format under 1000 words.
Be organized, informative, and clear."""


# === LangChain LLM ===
def get_llm():
    return ChatGroq(model_name=MODEL_NAME)


# === Read file ===
def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# === Write file ===
def write_file(content):
    os.makedirs(FINAL_NOTES_DIR, exist_ok= True)
    output_path = os.path.join(FINAL_NOTES_DIR, "notes.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Notes are saved at {output_path}")
    return output_path


# === Split text into chunks ===
def split_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


# === Summarize a chunk ===
def summarize_chunk(llm, chunk_text):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=chunk_text)
    ]
    response = llm.invoke(messages)
    return response.content.strip()


# === Final summary pass ===
# def summarize_all_chunks(llm, chunk_summaries):
#     combined = "\n\n".join(chunk_summaries)
#     messages = [
#         SystemMessage(content=FINAL_SUMMARY_PROMPT),
#         HumanMessage(content=combined)
#     ]
#     response = llm.invoke(messages)
#     return response.content.strip()

from langchain.schema import SystemMessage, HumanMessage

def summarize_all_chunks(llm, chunk_summaries, batch_size=2):
    """
    Summarize pre-summarized chunks in smaller batches to stay under token limits.
    No final summarization is done — the result is built progressively.
    """
    summary_so_far = ""

    for i in range(0, len(chunk_summaries), batch_size):
        batch = chunk_summaries[i:i + batch_size]
        combined = "\n\n".join(batch)

        # Build the prompt with current summary so far (if any) + new batch
        if summary_so_far:
            prompt_content = f"Existing summary:\n{summary_so_far}\n\nAdd this:\n{combined}\n\nCreate a concise combined summary:"
        else:
            prompt_content = f"{combined}\n\nSummarize this content:"

        messages = [
            SystemMessage(content=FINAL_SUMMARY_PROMPT),
            HumanMessage(content=prompt_content)
        ]

        response = llm.invoke(messages)
        summary_so_far = response.content.strip()

    return summary_so_far



# === Main function ===
def generate_final_notes(video_id):
    llm = get_llm()

    SUMMARY_PATH = f"data/summaries/{video_id}.txt"
    TRANSCRIPT_PATH = f"data/transcripts/{video_id}.txt"


    if not os.path.exists(TRANSCRIPT_PATH):
        raise FileNotFoundError(f"Transcript not found: {TRANSCRIPT_PATH}")

    if not os.path.exists(SUMMARY_PATH):
        raise FileNotFoundError(f"Frame summary not found: {SUMMARY_PATH}")

    transcript_text = read_file(TRANSCRIPT_PATH)
    frames_text = read_file(SUMMARY_PATH)

    full_input = f"Transcript:\n{transcript_text}\n\nFrame Summaries:\n{frames_text}"

    print("🔁 Splitting input into chunks...")
    chunks = split_text(full_input)

    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        print(f"🧠 Summarizing chunk {idx + 1}/{len(chunks)}...")
        summary = summarize_chunk(llm, chunk)
        chunk_summaries.append(summary)

    print("📚 Performing final summarization...")

    MAX_TOKENS = 8000
    RESERVED_FOR_SUMMARY = 2000   # Room for growing rolling summary
    CHUNK_SUMMARY_RATIO = 0.3     # 30% of original chunk size
    estimated_summary_size = int(CHUNK_SIZE * CHUNK_SUMMARY_RATIO)

    available_tokens = MAX_TOKENS - RESERVED_FOR_SUMMARY
    batch_size = max(1, math.floor(available_tokens / estimated_summary_size))

    final_notes = summarize_all_chunks(llm, chunk_summaries, batch_size)

    
    output_path =write_file(final_notes)

    # print(f"✅ Final notes saved to: {output_path}")
    return output_path  


# # === CLI Entry Point ===
# if __name__ == "__main__":
#     generate_final_notes("db64a120")  # change as needed
