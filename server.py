import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from mistralai import Mistral  # Use the new client

app = Flask(__name__, static_folder="static")
CORS(app)

# Access API key from Render's environment variables
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found. Ensure it's set in Render.")

client = Mistral(api_key=api_key)

# Serve index.html directly
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

# Handle AI chat requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": user_message}]
    )

    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
