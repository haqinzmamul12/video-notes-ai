from app.ui.upload import video_input
from app.processing.video_handler import save_uploaded_file, download_youtube_video
from app.processing.frame_extractor import extract_frames 
from app.processing.transcript_extractor import extract_transcript 
from app.llm.frame_summary import frame_summary_extractor
from app.llm.text_summariser import generate_final_notes
import streamlit as st



DATA_DIR = "data"

def main():
    user_input = video_input()

    if user_input:
        st.info("📥 Processing input...")

        try:
            # Generate a unique video ID
            # video_id = str(uuid.uuid4())[:8]

            if user_input["type"] == "youtube":
                video_path, video_id = download_youtube_video(user_input["data"])
                st.success(f"✅ YouTube video downloaded to {video_path}")

            elif user_input["type"] == "file":
                video_path = save_uploaded_file(user_input["data"])
                st.success(f"✅ Uploaded video saved to {video_path}")

            st.video(video_path)

            # Create output directories
            #video_id = os.path.splitext(os.path.basename(video_path))[0]
            

            # Extract frames
            st.info("🖼 Extracting frames...")
            extract_frames(video_id)
            #st.success(f"✅ Extracted {num_frames} frames.")
            #st.image(os.path.join(frame_output_dir, "frame_0.jpg"), caption="First extracted frame")

            # Extract transcript
            st.info("📝 Extracting transcript...")
            transcript_path = extract_transcript(video_id)
            with open(transcript_path, "r") as f:
                transcript = f.read()
            st.success(f"✅ Transcript extracted and saved to {transcript_path}")
            st.text_area("Transcript Preview", transcript)

            # Extract transcript
            st.info("📝 Creating Text Summary From Frames...")
            frame_summary_extractor(video_id) 

            # Extract transcript
            st.info("📝 Generating Final Notes...")
            notes_path =generate_final_notes(video_id)
            with open(notes_path, "r") as f:
                notes = f.read()
            st.success(f"✅ Transcript extracted and saved to {notes_path}")

            with st.expander("📄 Final Notes (Markdown Preview)", expanded= True):
                st.markdown(notes, unsafe_allow_html= True)
                st.download_button("💾 Download Notes", notes, file_name="video_notes.md")

        except Exception as e:
            st.error(f"❌ Failed to process video: {e}")

if __name__ == "__main__":
    main()
