from flask import Flask, request, jsonify
import yt_dlp
import time
import random
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend running"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"})

    try:
        time.sleep(random.uniform(1, 2))

        ydl_opts = {
            "format": "best",
            "quiet": True,
            "noplaylist": True,
            "http_headers": {
                "User-Agent": "Mozilla/5.0",
            },
            "retries": 3,
            "fragment_retries": 3,
            "socket_timeout": 15,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "title": info.get("title"),
            "duration": info.get("duration"),
            "url": info.get("url")
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ IMPORTANT FIX
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
