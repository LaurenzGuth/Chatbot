from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests

app = Flask(__name__)
CORS(app)
# Rasa-Server-URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"
@app.route("/")
def index():
    return "Chatbot Frontend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    sender_id = request.json.get("sender", "default")

    response = requests.post(RASA_SERVER_URL, json={
        "sender": sender_id,
        "message": user_message
    })

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Unable to process the message"}), response.status_code

@app.route("/restart", methods=["POST"])
def restart():
    response = requests.post(f"{RASA_SERVER_URL}/conversations/default/restart")
    if response.status_code == 200:
        return jsonify({"message": "Bot has been restarted"})
    else:
        return jsonify({"error": "Failed to restart the bot"}), response.status_code

if __name__ == "__main__":
    app.run(port=5000)