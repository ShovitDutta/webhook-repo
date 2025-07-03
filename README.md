# GitHub Webhook Event Monitor - Assignment Solution

## Overview
This solution implements a system that monitors GitHub events (Push, Pull Request, and Merge actions) via webhooks, stores them in MongoDB, and displays them in a real-time UI with Tailwind CSS styling.

![GitHub Events Monitor UI](screenshot.png)

## System Architecture
```
GitHub Repository (action-repo)
  │
  │ (Webhook events)
  ▼
Flask Server (webhook-repo) running on localhost:5000
  │
  │ (Store events)
  ▼
MongoDB running on localhost:27017
  │
  │ (Poll every 15s)
  ▼
Browser UI (http://localhost:5000)
```

## Features
- Real-time GitHub event monitoring (Push, PR, Merge)
- MongoDB storage with proper schema
- Auto-refreshing UI with Tailwind CSS styling
- Local development environment setup
- Responsive design for all devices
- Color-coded event types for quick recognition

## Setup Instructions

### Prerequisites
1. Python 3.7+
2. MongoDB Community Edition
3. ngrok (for local webhook testing)
4. Git

### Step 1: Set up MongoDB
1. Install MongoDB: https://www.mongodb.com/try/download/community
2. Start MongoDB service:
   ```bash
   # Mac
   brew services start mongodb-community
   
   # Windows (run as admin)
   net start MongoDB
   
   # Linux (Ubuntu)
   sudo systemctl start mongod
   ```

### Step 2: Clone and Set Up webhook-repo
```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo

# Create virtual environment
python -m venv venv

# Activate environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

### Step 3: Set Up ngrok
1. Download ngrok: https://ngrok.com/download
2. Run ngrok in a new terminal:
   ```bash
   ngrok http 5000
   ```
3. Copy the HTTPS URL (e.g., `https://abcd1234.ngrok.io`)

### Step 4: Create action-repo
1. Create a new GitHub repository
2. Go to Settings → Webhooks → Add webhook:
   - Payload URL: `https://<your-ngrok-id>.ngrok.io/webhook`
   - Content type: `application/json`
   - Events: Select "Send me everything" or individually select:
     - Push
     - Pull requests
     - Branch or tag creation (for merges)

### Step 5: Access the UI
Visit `http://localhost:5000` in your browser

## Testing the System
1. **Test Push Event**:
   ```bash
   git clone https://github.com/your-username/action-repo.git
   cd action-repo
   echo "Test" >> test.txt
   git add test.txt
   git commit -m "Test push"
   git push origin main
   ```

2. **Test Pull Request**:
   - Create a new branch: `git checkout -b test-pr`
   - Make changes and push
   - Create PR on GitHub

3. **Test Merge**:
   - Merge the PR on GitHub

## File Structure
```
webhook-repo/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Tailwind CSS UI
└── README.md
```

## MongoDB Schema
```javascript
{
  _id: ObjectId,         // MongoDB default ID
  request_id: String,    // Commit SHA or PR number
  author: String,        // GitHub username
  action: String,        // "PUSH", "PULL_REQUEST", or "MERGE"
  from_branch: String,   // Source branch (null for pushes)
  to_branch: String,     // Target branch
  timestamp: ISODate     // Event timestamp in UTC
}
```

## API Endpoints
- `POST /webhook` - GitHub webhook receiver
- `GET /` - UI dashboard
- `GET /events` - JSON API for events (used by UI)

## Troubleshooting
1. **No events showing up?**
   - Check ngrok is running and pointing to port 5000
   - Verify webhook setup in GitHub repository
   - Check Flask logs for errors
   - Ensure MongoDB service is running

2. **UI not updating?**
   - Verify JavaScript is enabled in browser
   - Check browser console for errors (F12)
   - Ensure the Flask app is running

3. **Database connection issues?**
   - Verify MongoDB is running: `mongo --eval "db.stats()"`
   - Check connection string in app.py

## Future Enhancements
- Add user authentication
- Implement pagination for event history
- Add filtering by event type
- Include repository name in events
- Add charts for event statistics

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.