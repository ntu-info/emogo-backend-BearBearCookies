# 📱 EmoGo Backend

This is the backend service for the **EmoGo** mobile application, built with **FastAPI** and **MongoDB**. It handles data collection (videos recording, emotion collection, GPS coordinates) and provides a dashboard for viewing and downloading the collected sessions.

## 🔗 Demo / Data Dashboard
**[Required]** Access the data-exporting page here (using mock data):
👉 **[EmoGo Backend Dashboard](https://emogo-backend-bearbearcookies.onrender.com)**

> **Note for TAs & Graders:**
> This service is deployed on **Render (Free Tier)**.
> * **Persistent Data:** All metadata (Sentiment, GPS, Timestamps) is stored in **MongoDB Atlas** and will **always** be visible.
> * **Ephemeral Data:** Video files are stored on the server's ephemeral filesystem. They **may be deleted** if the server spins down or restarts due to inactivity.
> * If video links return `404 Not Found`, it is due to this Render limitation. You can view the persistent GPS/Sentiment data on the dashboard, or run the provided `test_data_upload.py` script locally to re-upload fresh video content.

---

## 🚀 Features

1.  **Data Collection API**: Receives Vlogs (MP4), Emotion scores, and GPS coordinates from the EmoGo Frontend.
2.  **Dashboard UI**: A server-side rendered HTML page (Jinja2) to visualize and export data.
3.  **Cloud Database**: Connects to MongoDB Atlas for persistent storage of session metadata.

---

## 🛠️ Tech Stack

* **Language**: Python 3.9+
* **Framework**: FastAPI
* **Database**: MongoDB (via `motor` async driver)
* **Deployment**: Render Web Service

---

## 📂 Project Structure

```text
.
├── main.py                # Application entry point and API logic
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment configuration
├── test_data_upload.py    # Script to upload fake/test data
├── templates/
│   └── index.html         # Dashboard HTML template
└── uploads/               # Directory for storing temporary video files
```

## 🔌 API Endpoints

### 1. Dashboard
- **Endpoint:** `GET /`
- **Description:** Returns an HTML page listing all recorded sessions with download links.

### 2. Upload Session
- **Endpoint:** `POST /upload`
- **Content-Type:** `multipart/form-data`
- **Description:** Accepts video files and metadata from the frontend.

| Field | Type | Description |
| :--- | :--- | :--- |
| `sessionId` | String | Unique UUID for the session |
| `startTime` | String | ISO Timestamp |
| `emotionValue` | Int | User's emotion rating (0-5) |
| `duration` | Float | Duration of the recording in seconds |
| `latitude` | String | GPS Latitude (Optional) |
| `longitude` | String | GPS Longitude (Optional) |
| `file` | File | The video file (MP4) |

---

## 📱 Frontend Integration (Optional Goal)

The EmoGo Frontend (React Native/Expo) has been updated to "close the loop".

* **Automatic Upload**: When a user saves a session in the app, it automatically triggers a background upload to this backend.
* **Synchronization**: The app sends the recorded video along with the selected emotion and current location coordinates.
