from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins="*")

# 1. Update your Environment Variable in Render to GEMINI_API_KEY
# Get your key from https://aistudio.google.com/
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json()
    name = data.get("name") if data else None

    if not name:
        return jsonify({"error": "Please provide a name."}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key not configured."}), 500

    try:
        # 2. Updated to the Gemini REST endpoint
        # Using gemini-1.5-flash for the best free-tier performance
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "contents": [{
                    "parts": [{
                        "text": f"Generate a Chinese name for '{name}'. Return:\n1. Chinese characters\n2. Pinyin\n3. Meaning in 1 sentence"
                    }]
                }]
            },
            timeout=30
        )
        response.raise_for_status()
        
        # 3. Gemini's response structure is deeper: candidates -> content -> parts -> text
        json_res = response.json()
        result = json_res["candidates"][0]["content"]["parts"][0]["text"]
        
        return jsonify({"result": result})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out."}), 504
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "API is running! Send a POST request to /generate to use the Gemini tool."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)