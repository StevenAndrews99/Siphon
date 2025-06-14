import yt_dlp
import uuid
import os
import base64

def write_cookie_from_file():
    try:
        with open("cookies_b64.txt", "r") as f:
            encoded = f.read()
        decoded = base64.b64decode(encoded)
        os.makedirs("cookies", exist_ok=True)
        with open("cookies/youtube_cookies.txt", "wb") as out:
            out.write(decoded)
        print("✅ Cookies decoded and written to cookies/youtube_cookies.txt")
    except Exception as e:
        print(f"❌ Failed to decode/write cookies: {e}")

def download_video(url, format_choice, output_path):
    try:
        # Decode base64 cookies and save to file before download
        write_cookie_from_file()

        uid = str(uuid.uuid4())
        filename = f"{uid}.{format_choice}"
        filepath = os.path.join(output_path, filename)

        # Use the appropriate path to ffmpeg (update this if deploying to server)
        ffmpeg_path = "C:\\Users\\Steve\\OneDrive\\Desktop\\Siphon\\ffmpeg\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

        if format_choice == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': filepath,
                'ffmpeg_location': ffmpeg_path,
                'cookiefile': 'cookies/youtube_cookies.txt',
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
                'cookiefile': 'cookies/youtube_cookies.txt',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
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



