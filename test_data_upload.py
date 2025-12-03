import requests
import os

# 1. 設定你的 Render 網址
API_URL = "https://emogo-backend-bearbearcookies.onrender.com"

# 2. 指定真正的影片路徑 (根據你的截圖，影片在 video 資料夾內)
# 請確認你的資料夾結構是這樣，且該檔案真的存在
video_path = "video/landscape.mp4" 

# 檢查檔案是否存在
if not os.path.exists(video_path):
    print(f"❌ Error: 找不到影片檔 '{video_path}'。請確認檔案路徑是否正確。")
    exit()

# 3. 準備假資料 (Metadata)
payload = {
    "sessionId": "real_video_test_002",    # 改個 ID 區別一下
    "startTime": "2025-12-03T12:00:00",
    "emotionValue": 5,
    "duration": 20.0,
    "latitude": "25.0330",
    "longitude": "121.5654"
}

# 4. 發送請求
print(f"🚀 Uploading REAL video to {API_URL}/upload ...")

try:
    # 直接打開真正的影片檔
    with open(video_path, "rb") as video_file:
        files = {
            "file": ("landscape.mp4", video_file, "video/mp4")
        }
        
        response = requests.post(f"{API_URL}/upload", data=payload, files=files)
        
        if response.status_code == 200:
            print("✅ Success! Server responded:", response.json())
            print("👉 Now refresh your dashboard: ", API_URL)
        else:
            print(f"❌ Failed. Status: {response.status_code}")
            print("Response:", response.text)

except Exception as e:
    print(f"❌ Error: {e}")