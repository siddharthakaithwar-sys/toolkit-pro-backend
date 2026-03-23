from flask import Flask, request, jsonify
import yt_dlp
import time
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend running"

@app.route("/api/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    try:
        # random delay (anti-spam)
        time.sleep(random.uniform(1, 3))

        ydl_opts = {
            "format": "best",
            "quiet": True,
            "noplaylist": True,

            # 🔥 MOST IMPORTANT (429 fix attempt)
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            },

            # retry logic
            "retries": 3,
            "fragment_retries": 3,

            # network tuning
            "socket_timeout": 15,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # best direct URL
            video_url = info.get("url")

            return jsonify({
                "title": info.get("title"),
                "duration": info.get("duration"),
                "url": video_url
            })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
