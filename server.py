# -------| |---------------------------------------------------------------
import os
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
# -------| |---------------------------------------------------------------
code = Flask(__name__)
CORS(code)
# -------| |---------------------------------------------------------------
load_dotenv()
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
print(client.server_info())
db = client.github_events
events = db.events
# -------| |---------------------------------------------------------------
@code.route("/")
def index():
    return render_template("webhook.html")
# -------| |---------------------------------------------------------------
@code.route("/webhook", methods=["POST"])
def webhook():
    try:
        event = request.headers.get("X-GitHub-Event")
        payload = request.json
        if event == "push": process_push_event(payload)
        elif event == "pull_request": process_pull_request_event(payload)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500
# -------| |---------------------------------------------------------------
def process_push_event(payload):
    branch = payload["ref"].split("/")[-1]
    commit_id = payload["head_commit"]["id"] if "head_commit" in payload else "N/A"
    author = payload["pusher"]["name"] if "pusher" in payload else payload["sender"]["login"]
    timestamp = payload["head_commit"]["timestamp"] if "head_commit" in payload else datetime.now(timezone.utc).isoformat()
    event_data = {"request_id": commit_id, "author": author, "action": "PUSH", "from_branch": None, "to_branch": branch, "timestamp": datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")}
    events.insert_one(event_data)
    print(f"Stored PUSH event: {event_data}")
# -------| |---------------------------------------------------------------
def process_pull_request_event(payload):
    action = payload["action"]
    pr = payload["pull_request"]
    author = pr["user"]["login"]
    to_branch = pr["base"]["ref"]
    from_branch = pr["head"]["ref"]
    if action == "opened": timestamp = pr["created_at"]
    elif action == "closed": timestamp = pr["closed_at"] if "closed_at" in pr else datetime.now(timezone.utc).isoformat()
    else: return
    if action == "opened": event_type = "PULL_REQUEST"
    elif action == "closed" and pr.get("merged", False): event_type = "MERGE"
    else: return
    event_data = {"author": author, "action": event_type, "to_branch": to_branch, "from_branch": from_branch, "request_id": str(pr["number"]), "timestamp": datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")}
    events.insert_one(event_data)
    print(f"Stored {event_type} event: {event_data}")
# -------| |---------------------------------------------------------------
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
        print(f"Error fetching events: {str(e)}")
        return jsonify({"error": str(e)}), 500
# -------| |---------------------------------------------------------------
if __name__ == "__main__":
    code.run(host="0.0.0.0", port=5000, debug=True)
# -------| |---------------------------------------------------------------