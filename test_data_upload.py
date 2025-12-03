import requests
import os

# 1. 設定你的 Render 網址 (不要有最後的斜線 /)
API_URL = "https://emogo-backend-bearbearcookies.onrender.com"

# 2. 準備假資料
payload = {
    "sessionId": "test_session_fake_001",  # 假 ID
    "startTime": "2025-12-03T10:30:00",
    "emotionValue": 5,                     # 模擬心情 (0-5)
    "duration": 15.5,
    "latitude": "25.0330",
    "longitude": "121.5654"
}

# 3. 建立一個假的影片檔 (如果沒有現成的 mp4)
dummy_filename = "landscape.mp4"
with open(dummy_filename, "wb") as f:
    f.write(b"This is not a real video, just fake bytes for testing.")

# 4. 發送請求 (模擬 App 的行為)
print(f"🚀 Sending fake data to {API_URL}/upload ...")

try:
    with open(dummy_filename, "rb") as video_file:
        files = {
            "file": (dummy_filename, video_file, "video/landscape.mp4")
        }
        
        response = requests.post(f"{API_URL}/upload", data=payload, files=files)
        
        if response.status_code == 200:
            print("✅ Success! Server responded:", response.json())
            print("👉 Now check your dashboard: ", API_URL)
        else:
            print(f"❌ Failed. Status: {response.status_code}")
            print("Response:", response.text)

except Exception as e:
    print(f"❌ Error: {e}")

# 清理假檔案
if os.path.exists(dummy_filename):
    os.remove(dummy_filename)