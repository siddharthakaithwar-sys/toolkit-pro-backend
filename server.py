from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'service': 'ToolKit Pro YT-DLP API'})

@app.route('/api/download', methods=['GET'])
def get_download():
    url     = request.args.get('url', '')
    quality = request.args.get('quality', '720')
    fmt     = request.args.get('format', 'mp4')
    if not url:
        return jsonify({'error': 'URL required'}), 400
    try:
        if fmt == 'mp3':
            format_sel = 'bestaudio[ext=m4a]/bestaudio'
        elif quality == 'best':
            format_sel = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            format_sel = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
        ydl_opts = {'quiet': True, 'format': format_sel}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            dl_url = info.get('url') or (info.get('requested_formats') or [{}])[0].get('url', '')
            return jsonify({'url': dl_url, 'title': info.get('title', 'video'), 'ext': fmt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port