from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ========== Database Models ==========
class HostelInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(50), unique=True)
    response = db.Column(db.Text)

# ========== Chatbot Logic ==========
def hostel_bot_response(user_input):
    user_input = user_input.lower()

    keyword_map = {
        "rooms": ["room", "rooms", "single", "double", "triple"],
        "fees": ["fee", "fees", "charges", "cost"],
        "facilities": ["facility", "facilities", "service", "services"],
        "rules": ["rule", "rules", "regulations"],
        "location": ["location", "address", "where"],
        "contact": ["contact", "phone", "email", "number"]
    }

    for topic, keywords in keyword_map.items():
        if any(word in user_input for word in keywords):
            info = HostelInfo.query.filter_by(topic=topic).first()
            return info.response if info else f"No info available for {topic}."

    return (
        "Hi! I can help you with hostel info 🏠\n"
        "Try asking about:\n"
        "- Rooms\n"
        "- Fees\n"
        "- Facilities\n"
        "- Rules\n"
        "- Location\n"
        "- Contact details"
    )

# ========== Routes ==========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = hostel_bot_response(user_input)
    return jsonify({'reply': response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
