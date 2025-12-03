import os
from datetime import datetime
from typing import Optional
from bson import ObjectId

# 必須引入 GridFS 相關套件
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 1. MongoDB 連線設定
MONGO_URI = os.getenv("MONGO_URI") 
client = AsyncIOMotorClient(MONGO_URI)
db = client.emogo_db
collection = db.sessions

# 2. 初始化 GridFS (這是專門用來存檔案的 "桶子")
fs = AsyncIOMotorGridFSBucket(db)

# 設定 HTML 模板
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """
    Dashboard: 列出所有資料
    """
    sessions = await collection.find().sort("startTime", -1).to_list(50)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "sessions": sessions
    })

# --- 新增：專門用來「播放/下載」影片的網址 ---
@app.get("/video/{file_id}")
async def stream_video(file_id: str):
    """
    從 MongoDB GridFS 讀取影片並串流給瀏覽器
    """
    try:
        # 嘗試從 GridFS 開啟檔案
        grid_out = await fs.open_download_stream(ObjectId(file_id))
        
        # 回傳串流回應 (這樣瀏覽器可以直接播，不用等下載完)
        return StreamingResponse(
            content=grid_out, 
            media_type="video/mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Video not found")

@app.post("/upload")
async def upload_session(
    sessionId: str = Form(...),
    startTime: str = Form(...),
    emotionValue: int = Form(...),
    duration: float = Form(0),
    latitude: Optional[str] = Form(None),
    longitude: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    上傳：將影片直接寫入 MongoDB GridFS
    """
    # 1. 將影片檔案串流寫入 MongoDB
    # upload_from_stream 會回傳一個 file_id，這是影片在資料庫裡的唯一 ID
    file_id = await fs.upload_from_stream(
        filename=f"{sessionId}.mp4",
        source=file.file,
        metadata={"contentType": "video/mp4"}
    )
    
    # 2. 準備 metadata
    data = {
        "sessionId": sessionId,
        "startTime": startTime,
        "emotionValue": emotionValue,
        "duration": duration,
        "gps": {
            "latitude": latitude, 
            "longitude": longitude
        },
        # ⚠️ 這裡很重要：我們存的是專屬的 API 連結，而不是靜態檔案路徑
        "videoUrl": f"/video/{file_id}", 
        "gridfs_id": str(file_id), # 備份存一下 ID
        "uploadedAt": datetime.now()
    }
    
    # 3. 寫入資料庫
    await collection.insert_one(data)
    
    return {"status": "success", "message": "Uploaded to MongoDB GridFS"}