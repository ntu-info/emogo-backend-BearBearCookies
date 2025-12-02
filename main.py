import os
import shutil
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# 1. 建立上傳資料夾
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 2. 設定 HTML 模板
templates = Jinja2Templates(directory="templates")

# 3. MongoDB 連線
MONGO_URI = os.getenv("MONGO_URI") 
client = AsyncIOMotorClient(MONGO_URI)
db = client.emogo_db
collection = db.sessions

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """
    給 TA 看的 Dashboard
    """
    # 撈取資料，並按開始時間排序
    sessions = await collection.find().sort("startTime", -1).to_list(50)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "sessions": sessions
    })

@app.post("/upload")
async def upload_session(
    # ⚠️ 這裡的參數名稱已經改成和你前端完全一致
    sessionId: str = Form(...),
    startTime: str = Form(...),
    emotionValue: int = Form(...),
    duration: float = Form(0),
    latitude: Optional[str] = Form(None), # 接收字串較為彈性
    longitude: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    接收 App 上傳的資料
    """
    # 1. 儲存影片
    # 為了避免檔名重複，我們用 sessionId 來重新命名
    filename = f"{sessionId}.mp4"
    file_location = f"uploads/{filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. 準備寫入 MongoDB 的資料
    data = {
        "sessionId": sessionId,
        "startTime": startTime,
        "emotionValue": emotionValue, # 0-5 的數字
        "duration": duration,
        "gps": {
            "latitude": latitude, 
            "longitude": longitude
        },
        "videoUrl": f"/uploads/{filename}", # 給網頁用的連結
        "uploadedAt": datetime.now()
    }
    
    # 3. 寫入資料庫
    await collection.insert_one(data)
    
    return {"status": "success", "message": "Uploaded successfully"}