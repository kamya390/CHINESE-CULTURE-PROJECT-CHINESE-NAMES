from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins="*")

# This will look for GEMINI_API_KEY in your Render Environment Variables
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
        return jsonify({"error": "Gemini API key not configured in environment variables."}), 500

    try:
        # Using the v1 stable endpoint and gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Generate a creative and culturally accurate Chinese name for the English name '{name}'. "
                           f"Return the response in this format:\n"
                           f"1. Chinese Characters\n"
                           f"2. Pinyin\n"
                           f"3. A one-sentence explanation of the meaning."
                }]
            }]
        }

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        # Check if Google returned an error (like an invalid key or 404)
        if response.status_code != 200:
            return jsonify({
                "error": "Google API Error",
                "details": response.text
            }), response.status_code

        json_res = response.json()
        
        # Extracting the text from Gemini's nested JSON structure
        result = json_res["candidates"][0]["content"]["parts"][0]["text"]
        
        return jsonify({"result": result})

    except requests.exceptions.Timeout:
        return jsonify({"error": "The request to the AI timed out."}), 504
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Chinese Name Generator API is Live! Send POST requests to /generate."


if __name__ == "__main__":
    # Render uses the PORT environment variable, defaulting to 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)