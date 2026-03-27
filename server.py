from flask import Flask, request, jsonify
import yt_dlp
import time
import random
import os

app = Flask(__name__)

# -----------------------
# 🔹 BASIC ROUTES
# -----------------------

@app.route("/")
def home():
    return "Backend running"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# -----------------------
# 🔹 MAIN API
# -----------------------

@app.route("/api/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": "error",
            "message": "No URL provided"
        })

    try:
        # 🔹 random delay (anti-bot)
        time.sleep(random.uniform(2, 4))

        ydl_opts = {
            "format": "best",
            "quiet": True,
            "noplaylist": True,

            # 🔥 anti-bot headers
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept-Language": "en-US,en;q=0.9"
            },

            # 🔹 retry system
            "retries": 3,
            "fragment_retries": 3,

            # 🔹 stability
            "socket_timeout": 15,
            "nocheckcertificate": True,
            "ignoreerrors": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if not info:
            return jsonify({
                "status": "error",
                "message": "Failed to fetch video info (blocked or invalid)"
            })

        return jsonify({
            "status": "success",
            "title": info.get("title"),
            "duration": info.get("duration"),
            "url": info.get("url")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Extraction failed",
            "details": str(e)
        })


# -----------------------
# 🔹 RUN SERVER (IMPORTANT)
# -----------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
