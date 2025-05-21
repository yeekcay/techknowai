import os
from flask import Flask, session, request, jsonify, send_from_directory
from flask_cors import CORS
from mistralai import Mistral
from flask_session import Session

app = Flask(__name__, static_folder="static")
CORS(app)

# Configure Flask session
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.getenv("SECRET_KEY", "default_secret")  # Set a strong secret key
Session(app)

# Initialize Mistral AI client
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY missing. Ensure it's set in Render.")

client = Mistral(api_key=api_key)

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # Retrieve previous messages from session
    if "conversation_history" not in session:
        session["conversation_history"] = []

    session["conversation_history"].append({"role": "user", "content": user_message})

    # Send the full conversation history to Mistral AI
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=session["conversation_history"]
    )

    ai_response = response.choices[0].message.content

    # Store AI response in session history
    session["conversation_history"].append({"role": "assistant", "content": ai_response})

    return jsonify({"result": ai_response})

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("conversation_history", None)
    return jsonify({"message": "Conversation history cleared."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
