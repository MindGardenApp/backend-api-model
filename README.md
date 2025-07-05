# 🧠 Emotion Classifier & Supportive Chatbot API (Flask + Together AI)

This is a Flask-based backend API that leverages [Together AI](https://www.together.ai/) and LLaMA 3 (8B Chat) model to:

1. **Classify user emotions** from journal entries or personal messages.
2. **Respond empathetically** to user "curhatan" (emotional expressions) in Bahasa Indonesia.

---

## 📌 Endpoints

### `POST /predict` – Emotion Classification

Classifies a given text into one of six emotions: joy, anger, sadness, love, fear, or surprise.

#### ✅ Request
```json
{
  "content": "Isi curhatan atau pesan pengguna di sini"
}
```
#### 🔁 Response
```json
{
  "text": "Isi curhatan atau pesan pengguna di sini",
  "label": "joy",
  "score": 30,
  "raw_model_output": "1"
}
```

### `POST /curhat` – Empathetic Response

Classifies a given text into one of six emotions: joy, anger, sadness, love, fear, or surprise.

#### ✅ Request
```json
{
  "message": "Aku merasa lelah dan tidak tahu harus bagaimana lagi..."
}
```

#### 🔁 Response
```json
{
  "reply": "Saya mengerti perasaanmu. Kadang kita memang butuh waktu untuk diri sendiri. Jangan menyerah, kamu tidak sendirian."
}
```
