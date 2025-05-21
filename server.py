from flask import Flask, request, jsonify
from flask_cors import CORS
from mistralai import Mistral  # Use the new client

app = Flask(__name__)
CORS(app)

# Initialize Mistral AI client
api_key = "8V6o1W55NsHO8WcU80kjoaVemSVOV1SN"  # Replace with your actual key
client = Mistral(api_key=api_key)

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
    app.run(debug=True)
