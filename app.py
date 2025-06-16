from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        filename = str(uuid.uuid4()) + ".mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': filepath,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', error=None)

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run(debug=True)
