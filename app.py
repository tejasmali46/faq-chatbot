from flask import Flask, render_template, request, jsonify
from utils.chatbot import get_answer

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message", "")

    print("Received:", user_message)

    bot_reply = get_answer(user_message)

    print("Reply:", bot_reply)

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)