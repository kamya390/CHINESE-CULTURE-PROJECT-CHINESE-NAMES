from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.json.get("name")

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": f"Generate a Chinese name for '{name}' with characters, pinyin, and meaning."
                }
            ]
        }
    )

    data = response.json()
    result = data["choices"][0]["message"]["content"]

    return jsonify({"result": result})


@app.route("/")
def home():
    return "API is running!"