from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# === Together API Config ===
API_KEY = os.getenv("TOGETHER_API_KEY")
API_URL = "https://api.together.xyz/v1/chat/completions"

# === Mapping angka ke label & skor
label_mapping = {
    "1": "joy",
    "2": "anger",
    "3": "sadness",
    "4": "love",
    "5": "fear",
    "6": "surprise"
}

emotion_score = {
    "joy": 30,
    "love": 25,
    "surprise": 15,
    "sadness": -20,
    "anger": -30,
    "fear": -15
}

# === Prompt untuk klasifikasi emosi
EMOTION_PROMPT = (
    "Klasifikasikan teks curhatan ini sebagai perasaan bahagia, marah, sedih, jatuh cinta, takut, atau terkejut. "
    "Ketikkan 1 untuk bahagia, 2 untuk marah, 3 untuk sedih, 4 untuk jatuh cinta, 5 untuk takut, dan 6 untuk terkejut. "
    "Jangan berikan output apapun kecuali salah satu dari angka tersebut."
)

# === Endpoint Klasifikasi Emosi (NLP via Together)
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("content", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": EMOTION_PROMPT},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"].strip()
        emotion_label = label_mapping.get(reply, "unknown")
        score = emotion_score.get(emotion_label, 0)

        return jsonify({
            "text": text,
            "label": emotion_label,
            "score": score,
            "raw_model_output": reply
        })
    else:
        return jsonify({
            "error": "Gagal memanggil Together API",
            "details": response.text
        }), response.status_code

# === Endpoint untuk Curhat (Generatif)
SYSTEM_PROMPT = (
    "Kamu adalah asisten virtual yang sangat pengertian dan penuh empati. "
    "Jawab semua curhatan pengguna dalam Bahasa Indonesia dengan lembut, sopan, dan memberi semangat. "
    "Jangan gunakan Bahasa Inggris. Jangan mencampur Bahasa Indonesia dengan Bahasa Inggris. "
    "Tiga kalimat saja."
)

@app.route("/curhat", methods=["POST"])
def curhat():
    data = request.get_json()
    user_input = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"error": "Gagal memanggil Together API", "details": response.text}), response.status_code

# === Halaman Utama
@app.route("/")
def index():
    return "Server Flask aktif! Endpoint: /predict (klasifikasi emosi) & /curhat (respon empatik)"

# === Run Flask
if __name__ == "__main__":
    app.run(port=5000, debug=True)
