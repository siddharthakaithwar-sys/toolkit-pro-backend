from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

# ✅ CORS fix
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route("/")
def home():
    return "API Running 🚀"


@app.route("/api")
def api():
    url = request.args.get("url")

    if not url:
        return jsonify({
            "status": "error",
            "message": "No URL provided"
        }), 400

    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'format': 'best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # ✅ SMART FORMAT PICK
        formats = info.get("formats", [])
        best_url = None

        for f in formats:
            # video + audio दोनों हो
            if f.get("ext") == "mp4" and f.get("acodec") != "none":
                best_url = f.get("url")
                break

        # fallback
        if not best_url:
            best_url = info.get("url")

        return jsonify({
            "status": "success",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "download_url": best_url
        })

    except Exception as e:
        msg = str(e).lower()

        # ✅ better error messages
        if "private" in msg:
            error_msg = "Video is private"
        elif "sign in" in msg:
            error_msg = "Age restricted / login required"
        elif "unavailable" in msg:
            error_msg = "Video unavailable"
        else:
            error_msg = str(e)

        return jsonify({
            "status": "error",
            "message": error_msg
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
