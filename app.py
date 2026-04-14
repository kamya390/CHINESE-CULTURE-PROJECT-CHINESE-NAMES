from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Enable CORS so your frontend can communicate with this backend without being blocked
CORS(app)

# Pulls your API key from the environment variables set in Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate():
    # Retrieve the name sent from the frontend
    name = request.json.get("name")

    # If no name is provided, return a quick error
    if not name:
        return jsonify({"error": "Please provide a name."}), 400

    # Make the secure request to OpenAI
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
        }
    )

    # Parse the response from OpenAI
    data = response.json()
    result = data["choices"][0]["message"]["content"]

    # Send the final string back to the frontend
    return jsonify({"result": result})


@app.route("/")
def home():
    return "API is running! Send a POST request to /generate to use the tool."