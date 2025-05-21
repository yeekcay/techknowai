from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from mistralai import Mistral
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Initialize Mistral AI client
api_key = os.environ.get("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

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
