import yt_dlp
import uuid
import os

def download_video(url, format_choice, output_path):
    try:
        uid = str(uuid.uuid4())
        filename = f"{uid}.{format_choice}"
        filepath = os.path.join(output_path, filename)

        ffmpeg_path = "/usr/bin/ffmpeg"
        # ffmpeg_path = "C:/Users/Steve/OneDrive/Desktop/Siphon/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
        cookies_path = "cookies/cookies.txt"

        if format_choice == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': filepath,
                'ffmpeg_location': ffmpeg_path,
                'cookiefile': cookies_path,
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
                'ffmpeg_location': ffmpeg_path,
                'cookiefile': cookies_path,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',  # ✅ This works across all setups
                    'preferedformat': 'mp4',
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


