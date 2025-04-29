from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ElevenLabs API key (for now, hardcoded — we'll protect later)
ELEVENLABS_API_KEY = "sk_56265d1be67a0367a61d1c6ba47359cdd4170a904da54dff"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # We'll pick a voice shortly!

@app.route('/')
def home():
    return "Welcome to the Voice Note Organizer API!"

@app.route('/generate-voice', methods=['POST'])
def generate_voice():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

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
        with open(filename, "wb") as f:
            f.write(response.content)
        return jsonify({"message": "Voice generated", "file": filename}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
