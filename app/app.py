# app/app.py
from flask import Flask, jsonify, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Database config (SQLite file in /data for persistence when containerized)
DB_PATH = os.environ.get("DB_PATH", "/data/feedback.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models (importing inline to keep single-file simple)
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }

def init_db():
    # Ensure directory exists
    dirpath = os.path.dirname(DB_PATH)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    db.create_all()

# Initialize database on app startup (Flask 3.x replacement)
with app.app_context():
    init_db()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/feedback", methods=["GET"])
def list_feedback():
    # optional query param ?limit=20
    limit = request.args.get("limit", default=100, type=int)
    items = Feedback.query.order_by(Feedback.created_at.desc()).limit(limit).all()
    return jsonify([i.to_dict() for i in items]), 200

@app.route("/api/feedback", methods=["POST"])
def create_feedback():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not message:
        return jsonify({"error": "name and message are required"}), 400

    fb = Feedback(name=name, email=email or None, message=message)
    db.session.add(fb)
    db.session.commit()
    return jsonify(fb.to_dict()), 201

# health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # listen on 0.0.0.0 for container usage
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
