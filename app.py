import streamlit as st
import yt_dlp
import subprocess
import os
import uuid

st.set_page_config(page_title="🎬 YouTube Clip Trimmer", layout="centered")
st.title("🎬 YouTube Clip Trimmer")

url = st.text_input("🔗 Enter YouTube URL")
start_time = st.text_input("⏱️ Start Time (HH:MM:SS)", value="00:00:00")
end_time = st.text_input("⏱️ End Time (HH:MM:SS)", value="00:00:10")

if st.button("✂️ Trim Video"):
    if url and start_time and end_time:
        unique_id = str(uuid.uuid4())
        download_file = f"video_{unique_id}.mp4"
        output_file = f"clip_{unique_id}.mp4"

        st.info("📥 Downloading video...")
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': download_file,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        st.info("✂️ Trimming video with FFMPEG...")

        # ✅ Re-encode both video and audio properly for compatibility
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', download_file,
            '-ss', start_time,
            '-to', end_time,
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            output_file
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        st.success("✅ Done! Preview or Download below:")

        # ✅ Video Preview
        st.video(output_file)

        # ✅ Download Button with correct MIME type
        with open(output_file, "rb") as file:
            st.download_button(
                label="📥 Download Trimmed Clip",
                data=file,
                file_name="trimmed_clip.mp4",
                mime="video/mp4"
            )

        # ✅ Cleanup
        os.remove(download_file)
        os.remove(output_file)

    else:
        st.warning("⚠️ Please fill in all the fields.")
