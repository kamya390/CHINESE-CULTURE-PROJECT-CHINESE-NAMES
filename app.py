from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins="*")

# 1. Get a free key from https://console.groq.com/
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name") if data else None

    if not name:
        return jsonify({"error": "Please provide a name."}), 400

    if not GROQ_API_KEY:
        return jsonify({"error": "Groq API key not configured."}), 500

    try:
        # 2. Changed the URL to Groq's endpoint
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                # 3. Changed the model to Llama 3 (Free on Groq)
                "model": "llama-3.3-70b-versatile",
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
        # Better debugging: print the error to your terminal
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "API is running! Send a POST request to /generate to use the Groq tool."


if __name__ == "__main__":
    # Standard Flask port is 5000; keeping 10000 as per your script
    app.run(host="0.0.0.0", port=10000)