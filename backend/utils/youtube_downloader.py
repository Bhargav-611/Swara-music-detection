import yt_dlp
import os

def download_youtube_audio(youtube_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)
        wav_path = os.path.splitext(filename)[0] + ".wav"

    return wav_path, info.get("title", "Unknown")
