from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate-voice', methods=['POST'])
def generate_voice():
    text = request.form.get('text')
    if not text:
        return redirect(url_for('index'))

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        filename = "generated_voice.mp3"
        filepath = os.path.join("static", filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        return render_template("index.html", audio_file=filename)
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
