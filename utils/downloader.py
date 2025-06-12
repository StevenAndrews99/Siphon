import yt_dlp
import uuid
import os

def download_video(url, format_choice, output_path):
    try:
        uid = str(uuid.uuid4())
        filename = f"{uid}.{format_choice}"
        filepath = os.path.join(output_path, filename)

        if format_choice == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': filepath,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }

        elif format_choice == 'mp4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': filepath,
                'postprocessors': [{
                    'key': 'FFmpegVideoReencoder',
                    'preferredformat': 'mp4',
                }],
                'quiet': True,
            }

        else:
            return None, "Invalid format selected."

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return filename, None

    except Exception as e:
        return None, str(e)

