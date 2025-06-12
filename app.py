from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from utils.downloader import download_video
import os
import uuid
import yt_dlp
import time

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

# Platform detection
def detect_platform(url):
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url:
        return "YouTube"
    elif "tiktok.com" in url:
        return "TikTok"
    elif "instagram.com" in url:
        return "Instagram"
    else:
        return "Unknown"

@app.route('/')
def index():
    return render_template("index.html", platform=None)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['youtube_url']
    format_choice = request.form['format']
    platform = detect_platform(url)

    filename, error = download_video(url, format_choice, app.config["DOWNLOAD_FOLDER"])

    if error:
        return f"Error: {error}", 400

    # Instead of sending the file immediately, redirect to an intermediate page
    return redirect(url_for("prepare_download", filename=filename))

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True)

@app.route('/prepare/<filename>')
def prepare_download(filename):
    return render_template("prepare.html", filename=filename)

@app.route('/fetch_metadata', methods=['POST'])
def fetch_metadata():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'platform': detect_platform(url)
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🧼 Auto-delete old files
def cleanup_old_files(folder_path, max_age_seconds=3600):
    now = time.time()

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            file_age = now - os.path.getmtime(filepath)
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    print(f"Deleted old file: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")

import subprocess
from flask import Response

@app.route("/debug_ffmpeg")
def debug_ffmpeg():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            return Response(f"<pre>{result.stdout}</pre>", mimetype="text/html")
        else:
            return Response(f"<pre>FFmpeg not found:\n{result.stderr}</pre>", mimetype="text/html")
    except Exception as e:
        return Response(f"<pre>Error running ffmpeg:\n{str(e)}</pre>", mimetype="text/html")

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    cleanup_old_files(DOWNLOAD_FOLDER, max_age_seconds=3600)

    app.run(debug=True)

