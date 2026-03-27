from flask import Flask, request, jsonify
import yt_dlp
import time
import random
import os

app = Flask(__name__)

# 🔥 in-memory cache
cache = {}

def extract_video(url):
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "noplaylist": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0",
        },
        "retries": 2,
        "fragment_retries": 2,
        "socket_timeout": 10,
        "nocheckcertificate": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

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
        return jsonify({
            "status": "error",
            "message": "No URL provided"
        })

    # 🔥 cache hit
    if url in cache:
        return jsonify({
            "status": "cached",
            "data": cache[url]
        })

    # 🔥 retry system (3 attempts)
    for attempt in range(3):
        try:
            time.sleep(random.uniform(2, 5))

            info = extract_video(url)

            if not info:
                continue

            result = {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "url": info.get("url")
            }

            cache[url] = result

            return jsonify({
                "status": "success",
                "data": result
            })

        except Exception as e:
            error_msg = str(e)

            # 🔥 अगर YouTube block करे
            if "Sign in to confirm" in error_msg:
                return jsonify({
                    "status": "blocked",
                    "message": "YouTube blocked this request",
                    "reason": "Cloud IP detected as bot",
                    "suggestion": "Try later or different video"
                })

            # retry continue
            continue

    # 🔥 final fallback
    return jsonify({
        "status": "failed",
        "message": "All attempts failed",
        "note": "This is a platform limitation, not code issue"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
