"""
JARVIS Personal AI Assistant — Private Backend API
Single-owner secure application
Works on Railway + Localhost
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import jwt
import os

# ─────────────────────────────────────────────
# APP CONFIG
# ─────────────────────────────────────────────

app = Flask(__name__)

# Environment-safe config
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-secret-key")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///jarvis.db")

# Fix Railway postgres
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)

# ─────────────────────────────────────────────
# OWNER CONFIG
# ─────────────────────────────────────────────

OWNER_EMAIL    = os.environ.get("OWNER_EMAIL", "your@email.com")
OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD", "Sethu123!")
OWNER_NAME     = os.environ.get("OWNER_NAME", "Sir")

# ─────────────────────────────────────────────
# DATABASE MODELS
# ─────────────────────────────────────────────

class Task(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    text       = db.Column(db.String(500), nullable=False)
    completed  = db.Column(db.Boolean, default=False)
    priority   = db.Column(db.String(20), default="medium")
    due_date   = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat()
        }

# ─────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────

def generate_token():
    return jwt.encode(
        {
            "email": OWNER_EMAIL,
            "exp": datetime.utcnow() + timedelta(days=30)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────────

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").lower().strip()
    password = data.get("password", "")

    if email != OWNER_EMAIL.lower():
        return jsonify({"error": "Access denied — private application"}), 403

    if password != OWNER_PASSWORD:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "token": generate_token(),
        "name": OWNER_NAME,
        "email": OWNER_EMAIL
    })

@app.route("/api/auth/verify", methods=["GET"])
@token_required
def verify():
    return jsonify({"valid": True, "name": OWNER_NAME})

# ─────────────────────────────────────────────
# TASK ROUTES
# ─────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
@token_required
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])

@app.route("/api/tasks", methods=["POST"])
@token_required
def create_task():
    data = request.get_json() or {}
    if not data.get("text"):
        return jsonify({"error": "Text required"}), 400

    task = Task(
        text=data["text"],
        priority=data.get("priority", "medium"),
        due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@token_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json() or {}

    if "text" in data:
        task.text = data["text"]
    if "completed" in data:
        task.completed = data["completed"]
    if "priority" in data:
        task.priority = data["priority"]

    db.session.commit()
    return jsonify(task.to_dict())

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"ok": True})

# ─────────────────────────────────────────────
# HEALTH CHECK (IMPORTANT FOR RAILWAY)
# ─────────────────────────────────────────────

@app.route("/")
def root():
    return jsonify({"status": "running", "app": "JARVIS"})

@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "version": "2.0.0"})

# ─────────────────────────────────────────────
# INIT DATABASE
# ─────────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Database ready")

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Running on port {port}")
    app.run(host="0.0.0.0", port=port)