# =========|Crafted By Shovit Dutta|===================================================
import os
import hmac
import logging
import hashlib
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
from colorama import Fore, Style, init
init()
# =========|Crafted By Shovit Dutta|===================================================
code = Flask(__name__)
CORS(code)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"{Fore.CYAN}Loading environment variables...{Style.RESET_ALL}")
load_dotenv()
mongo_url = os.getenv("MONGO_URL")
webhook_secret = os.getenv("WEBHOOK_SECRET")
logger.info(f"{Fore.GREEN}Environment variables loaded.{Style.RESET_ALL}")
client = MongoClient(mongo_url)
logger.info(f"{Fore.GREEN}Connected to MongoDB: {client.server_info()}{Style.RESET_ALL}")
db = client.github_events
events = db.events
# =========|Crafted By Shovit Dutta|===================================================
@code.route("/")
def index():
    logger.info(f"{Fore.CYAN}Serving webhook.html for index route.{Style.RESET_ALL}")
    return render_template("webhook.html")
# =========|Crafted By Shovit Dutta|===================================================
@code.route("/webhook", methods=["POST"])
def webhook():
    logger.info(f"{Fore.CYAN}Webhook received. Verifying signature...{Style.RESET_ALL}")
    if not verify_signature(request):
        logger.warning(f"{Fore.YELLOW}Invalid signature received for webhook.{Style.RESET_ALL}")
        return jsonify({"error": "Invalid signature"}), 403
    logger.info(f"{Fore.GREEN}Signature verified successfully.{Style.RESET_ALL}")
    try:
        event = request.headers.get("X-GitHub-Event")
        payload = request.json
        event_data = {
            "action": event,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc)
        }
        logger.info(f"{Fore.CYAN}Storing %s event in MongoDB...{Style.RESET_ALL}", event)
        events.insert_one(event_data)
        logger.info(f"{Fore.GREEN}Stored %s event: %s{Style.RESET_ALL}", event, event_data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"{Fore.RED}Error processing webhook: %s{Style.RESET_ALL}", str(e))
        return jsonify({"error": str(e)}), 500
def verify_signature(request):
    if not webhook_secret:
        logger.info(f"{Fore.YELLOW}WEBHOOK_SECRET not set, skipping signature verification.{Style.RESET_ALL}")
        return True
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        logger.warning(f"{Fore.YELLOW}X-Hub-Signature-256 header missing.{Style.RESET_ALL}")
        return False
    expected_signature = "sha256=" + hmac.new(webhook_secret.encode(), request.data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
# =========|Crafted By Shovit Dutta|===================================================
@code.route("/events", methods=["GET"])
def get_events():
    logger.info(f"{Fore.CYAN}Fetching latest events from MongoDB...{Style.RESET_ALL}")
    try:
        latest_events = list(events.find().sort("timestamp", -1).limit(10))
        logger.info(f"{Fore.GREEN}Successfully fetched %d events.{Style.RESET_ALL}", len(latest_events))
        for event in latest_events:
            event["_id"] = str(event["_id"])
            timestamp = event["timestamp"]
            day = timestamp.day
            suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
            formatted_time = timestamp.strftime(f"%d{suffix} %B %Y - %I:%M %p UTC")
            event["timestamp"] = formatted_time
        return jsonify(latest_events)
    except Exception as e:
        logger.error(f"{Fore.RED}Error fetching events: %s{Style.RESET_ALL}", str(e))
        return jsonify({"error": str(e)}), 500
# =========|Crafted By Shovit Dutta|===================================================
if __name__ == "__main__":
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    code.run(host="0.0.0.0", port=5000, debug=True)
# =========|Crafted By Shovit Dutta|===================================================