# GitHub Events Monitor 🚀

This project is a robust GitHub Events Monitor designed to capture, store, and display GitHub webhook payloads in real-time. It provides a dynamic web interface to visualize events from your repositories, offering insights into various activities such as pushes, pull requests, and more.

## Features ✨

*   **Real-time Event Monitoring:** Dynamically displays GitHub events as they occur. ⚡
*   **Webhook Integration:** Receives and processes GitHub webhook payloads securely. 🔗
*   **Database Persistence:** Stores all incoming event data in a MongoDB database for historical tracking. 💾
*   **User-Friendly Interface:** A clean and intuitive web interface to browse recent events. 🖥️
*   **Event Details:** Displays key information for each event, including author, event type, commit messages, and branch names. 🔍
*   **Interactive Elements:** Clickable event entries to directly navigate to the corresponding GitHub URL. 🖱️
*   **Connection Status:** Provides visual feedback on the frontend's connection status to the backend. 🟢
*   **Database Cleaning Utility:** A simple script to clear the event database. 🧹

<div align="center">
  <img src="preview.png" alt="Preview">
</div>

## Technologies Used 🛠️

### Backend 🐍
*   **Python:** The core programming language for the server.
*   **Flask:** A lightweight web framework for building the backend API.
*   **pymongo:** Python driver for MongoDB, used for database interactions.
*   **python-dotenv:** For managing environment variables.
*   **Flask-CORS:** Enables Cross-Origin Resource Sharing for frontend-backend communication.
*   **colorama:** For colored terminal output (e.g., logging).
*   **gunicorn:** A WSGI HTTP Server for UNIX, used for production deployment.

### Frontend 🌐
*   **HTML:** Structure of the web interface.
*   **CSS:** Styling of the web interface.
*   **JavaScript:** Powers the dynamic fetching and rendering of events.
*   **Tailwind CSS (via CDN):** A utility-first CSS framework for rapid UI development.
*   **Font Awesome (via CDN):** Provides scalable vector icons.

### Database 🗄️
*   **MongoDB:** A NoSQL database used to store GitHub event payloads.

### Development Tools 🧑‍💻
*   **Prettier:** An opinionated code formatter for maintaining consistent code style.

## Getting Started 🚀

Follow these instructions to set up and run the GitHub Events Monitor on your local machine.

### Prerequisites ✅

Before you begin, ensure you have the following installed:

*   **Python 3.x:** Download from [python.org](https://www.python.org/downloads/).
*   **pip:** Python's package installer (usually comes with Python 3.x).
*   **MongoDB Instance:** A running MongoDB database. You can install it locally or use a cloud service like MongoDB Atlas.

### Installation ⬇️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/github-events-monitor.git
    cd github-events-monitor
    ```
    *(Note: Replace `https://github.com/your-username/github-events-monitor.git` with the actual repository URL if available.)*

2.  **Install Python dependencies:**
    First, ensure your `requirements.txt` file contains the necessary packages. If not, you might need to create or correct it.
    ```
    Flask
    pymongo[srv]
    python-dotenv
    Flask-CORS
    colorama
    gunicorn
    ```
    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

### Environment Configuration ⚙️

Create a file named `.env` in the project root directory and add the following environment variables:

```dotenv
MONGO_URL="mongodb://localhost:27017/"
WEBHOOK_SECRET="your_github_secret_token"
```
*   Replace `"mongodb://localhost:27017/"` with your MongoDB connection string.
*   Replace `"your_github_secret_token"` with a strong, unique secret token. This token will be used to verify GitHub webhook signatures.

### Running the Backend Server 🏃‍♀️

You can run the Flask backend in development mode or using Gunicorn for production.

*   **Development Mode:**
    ```bash
    python server.py
    ```
    The server will typically run on `http://localhost:5000`.

*   **Production Mode (using Gunicorn):**
    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 server:code
    ```
    This command runs the server with 4 worker processes, binding to all network interfaces on port 5000.

### Configure GitHub Webhook 🎣

To receive events, you need to configure a webhook in your GitHub repository:

1.  Navigate to your GitHub repository.
2.  Go to **Settings** > **Webhooks**.
3.  Click **Add webhook**.
4.  **Payload URL:** Enter the URL where your server is accessible (e.g., `http://your-server-ip:5000/webhook`). If running locally, you might need a tool like ngrok to expose your local server to the internet.
5.  **Content type:** Select `application/json`.
6.  **Secret:** Enter the `WEBHOOK_SECRET` you defined in your `.env` file.
7.  **Which events would you like to trigger this webhook?**: Select "Let me select individual events." and choose the events you want to monitor (e.g., `Pushes`, `Pull requests`, `Issues`).
8.  Click **Add webhook**.

### Accessing the Frontend 🖥️

Once the backend server is running, open your web browser and navigate to:

```
http://localhost:5000
```

You should see the GitHub Events Monitor interface.

### Triggering Events 🔔

Perform actions in your configured GitHub repository (e.g., push a commit, open a pull request, create an issue) to trigger webhook events. These events should then appear dynamically on the web interface.

### Cleaning Database (Optional) 🗑️

To clear all stored GitHub events from the MongoDB database, run the utility script:

```bash
python cleandb.py
```
**Caution:** This will permanently delete all data in the `github_events` database.

## Usage 💡

Once the server is running and the GitHub webhook is configured, simply navigate to `http://localhost:5000` in your browser. The frontend will automatically fetch and display new events as they are triggered in your GitHub repository.

*   **View Events:** Events will appear in a list, showing details like the event type, author, and a brief description. 👀
*   **Open on GitHub:** Click on any event entry to open the corresponding page on GitHub in a new tab, providing more context. 🔗
*   **Monitor Connection:** Observe the connection status indicator on the page to ensure the frontend is successfully communicating with the backend. 🟢

## Contributing 🤝

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: A `LICENSE` file is not included in the provided file list. You may need to create one if you wish to specify a license.)*