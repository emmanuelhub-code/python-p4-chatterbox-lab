from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Message
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# ---------------------------
# Routes
# ---------------------------

# GET /messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# POST /messages
@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    msg = Message(body=data["body"], username=data["username"])
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_dict()), 201

# PATCH /messages/<int:id>
@app.route("/messages/<int:id>", methods=["PATCH"])
def update_message(id):
    data = request.get_json()
    msg = Message.query.get_or_404(id)
    if "body" in data:
        msg.body = data["body"]
    db.session.commit()
    return jsonify(msg.to_dict()), 200

# DELETE /messages/<int:id>
@app.route("/messages/<int:id>", methods=["DELETE"])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return "", 204

# Run the app
if __name__ == "__main__":
    app.run(port=5555, debug=True)
