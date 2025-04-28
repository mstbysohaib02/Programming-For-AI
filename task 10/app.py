from flask import Flask, render_template, request, jsonify, session
from chatbot import get_response

app = Flask(__name__)
app.secret_key = "your_secret_key" 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input = request.form["msg"]
    last_topic = session.get("last_topic")

    response, new_topic = get_response(user_input, last_topic)
    if new_topic:
        session["last_topic"] = new_topic

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
