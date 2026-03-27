from flask import Flask, request, jsonify
import yt_dlp
import requests

app = Flask(__name__)

# 🔥 CHANGE THIS (your local worker URL)
LOCAL_WORKER = "http://YOUR_IP:5000/local-download"

@app.route("/")
def home():
    return "Backend running"

def fetch_with_ytdlp(url):
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def try_local(url):
    try:
        res = requests.get(LOCAL_WORKER, params={"url": url}, timeout=10)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/api/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"})

    # 🔥 TRY CLOUD FIRST
    try:
        info = fetch_with_ytdlp(url)

        return jsonify({
            "status": "success",
            "source": "cloud",
            "title": info.get("title"),
            "url": info.get("url")
        })

    except Exception as e:
        error_msg = str(e)

        # 🔥 IF BLOCKED → FALLBACK
        if "bot" in error_msg.lower() or "sign in" in error_msg.lower():
            local = try_local(url)

            return jsonify({
                "status": "fallback",
                "reason": "cloud_blocked",
                "local_result": local
            })

        return jsonify({
            "status": "error",
            "message": error_msg
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
