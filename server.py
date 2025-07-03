import os
import logging
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
import hmac
import hashlib

code = Flask(__name__)
CORS(code)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URL")
webhook_secret = os.getenv("WEBHOOK_SECRET")  # Add this to your .env file

# MongoDB connection
client = MongoClient(mongo_url)
logger.info("Connected to MongoDB: %s", client.server_info())
db = client.github_events
events = db.events

@code.route("/", methods=["POST"])
def webhook():
    # Verify webhook signature
    if not verify_signature(request):
        return jsonify({"error": "Invalid signature"}), 403

    try:
        event = request.headers.get("X-GitHub-Event")
        payload = request.json
        if event == "push":
            process_push_event(payload)
        elif event == "pull_request":
            process_pull_request_event(payload)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error("Error processing webhook: %s", str(e))
        return jsonify({"error": str(e)}), 500

def verify_signature(request):
    if not webhook_secret:
        return True  # Skip verification if no secret is set

    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        return False

    expected_signature = "sha256=" + hmac.new(
        webhook_secret.encode(), request.data, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

def process_push_event(payload):
    branch = payload["ref"].split("/")[-1]
    commit_id = payload["head_commit"]["id"] if "head_commit" in payload else "N/A"
    author = payload["pusher"]["name"] if "pusher" in payload else payload["sender"]["login"]
    # Use pushed_at from repository if available, fallback to head_commit timestamp or current time
    timestamp = payload["repository"].get("pushed_at") or (payload["head_commit"].get("timestamp") if "head_commit" in payload else datetime.now(timezone.utc))
    if isinstance(timestamp, str):
        # Handle both GitHub format (2025-07-03T07:16:00Z) and ISO format (2025-07-03T07:17:40.981751+00:00)
        try:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            timestamp = datetime.fromisoformat(timestamp.replace("+00:00", "Z"))
    elif isinstance(timestamp, int):  # Handle Unix timestamp from pushed_at
        timestamp = datetime.fromtimestamp(timestamp, timezone.utc)
    event_data = {
        "request_id": commit_id,
        "author": author,
        "action": "PUSH",
        "from_branch": None,
        "to_branch": branch,
        "timestamp": timestamp
    }
    events.insert_one(event_data)
    logger.info("Stored PUSH event: %s", event_data)

def process_pull_request_event(payload):
    action = payload["action"]
    pr = payload["pull_request"]
    author = pr["user"]["login"]
    to_branch = pr["base"]["ref"]
    from_branch = pr["head"]["ref"]
    if action == "opened":
        timestamp = pr["created_at"]
        event_type = "PULL_REQUEST"
    elif action == "closed" and pr.get("merged", False):
        timestamp = pr["merged_at"] if "merged_at" in pr else pr["closed_at"]
        event_type = "MERGE"
    else:
        return
    # Handle timestamp format
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    event_data = {
        "author": author,
        "action": event_type,
        "to_branch": to_branch,
        "from_branch": from_branch,
        "request_id": str(pr["number"]),
        "timestamp": timestamp
    }
    events.insert_one(event_data)
    logger.info("Stored %s event: %s", event_type, event_data)

@code.route("/webhook")
def index():
    return render_template("webhook.html")

@code.route("/events", methods=["GET"])
def get_events():
    try:
        latest_events = list(events.find().sort("timestamp", -1).limit(10))
        for event in latest_events:
            event["_id"] = str(event["_id"])
            timestamp = event["timestamp"]
            day = timestamp.day
            suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            formatted_time = timestamp.strftime(f"%d{suffix} %B %Y - %I:%M %p UTC")
            event["timestamp"] = formatted_time
        return jsonify(latest_events)
    except Exception as e:
        logger.error("Error fetching events: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    code.run(host="0.0.0.0", port=5000, debug=True)