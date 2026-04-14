from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins="*")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name") if data else None

    if not name:
        return jsonify({"error": "Please provide a name."}), 400

    if not OPENAI_API_KEY:
        return jsonify({"error": "API key not configured."}), 500

    try:
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
                        "content": f"Generate a Chinese name for '{name}'. Return:\n1. Chinese characters\n2. Pinyin\n3. Meaning in 1 sentence"
                    }
                ]
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        return jsonify({"result": result})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "API is running! Send a POST request to /generate to use the tool."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)