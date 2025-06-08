import sys
import os
YOLOV5_DIR = os.path.join(os.path.dirname(__file__), "../yolov5")
sys.path.append(YOLOV5_DIR)
sys.path.append(os.path.abspath(os.path.join(YOLOV5_DIR, "..")))  # 加入 backend 目录

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List, Optional#List和Optional是Python的类型注解，用于指定变量类型
from PIL import Image
import torch
import io
import os
from config.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.models import User, Video, Log, DetectionResult  # 修正导入路径
from fastapi.middleware.cors import CORSMiddleware
import shutil
from datetime import datetime
import numpy as np
from yolov5.utils.general import non_max_suppression, scale_boxes, check_img_size
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载模型（修正路径）
MODEL_PATH = "runs/train/gpu_run/weights/best.pt"

# 使用 YOLOv5 官方推荐方式加载模型
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device

# 选择设备
device = select_device('cpu')  # 或 'cuda:0' 如果有 GPU

# 加载模型
if os.path.exists(MODEL_PATH):
    model = DetectMultiBackend(MODEL_PATH, device=device)
else:
    model = DetectMultiBackend(os.path.join(YOLOV5_DIR, 'yolov5s.pt'), device=device)

# 设置推理参数
stride = int(model.stride)
imgsz = check_img_size(640, s=stride)  # 检查图片大小

# 预热模型
model.warmup(imgsz=(1, 3, imgsz, imgsz))

VIDEOS_DIR = os.path.join(os.path.dirname(__file__), "../videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello World! 河道漂浮物检测系统后端已启动"}

# 1. 用户相关接口
@app.post("/api/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user_id": new_user.id, "username": new_user.username, "role": new_user.role}

@app.post("/api/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    用户登录接口
    """
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"user_id": user.id, "token": "mock_token"}

@app.get("/api/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户信息接口
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": str(user.created_at)
    }

@app.put("/api/users/{user_id}")
def update_user(user_id: int, username: str = Form(None), password: str = Form(None), role: str = Form(None), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if username:
        user.username = username
    if password:
        user.password = password
    if role:
        user.role = role
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "username": user.username, "role": user.role, "created_at": str(user.created_at)}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 删除用户相关视频和日志
    db.query(Video).filter(Video.user_id == user_id).delete()
    db.query(Log).filter(Log.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

# 2. 视频相关接口
@app.post("/api/videos/upload")
def upload_video(user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    filename = f"{user_id}_{file.filename}"
    save_path = os.path.join(VIDEOS_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    video = Video(user_id=user_id, video_path=filename, status="pending")
    db.add(video)
    db.commit()
    db.refresh(video)
    # 上传视频成功后
    log = Log(user_id=user_id, action="upload_video", action_time=datetime.utcnow())
    db.add(log)
    db.commit()
    return {"video_id": video.id, "video_path": filename, "status": video.status}

@app.get("/api/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    return {"video_id": video.id, "user_id": video.user_id, "video_path": video.video_path, "upload_time": str(video.upload_time), "status": video.status}

@app.get("/api/videos/user/{user_id}")
def get_user_videos(user_id: int, db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.user_id == user_id).all()
    return [{"video_id": v.id, "video_path": v.video_path, "upload_time": str(v.upload_time), "status": v.status} for v in videos]

@app.delete("/api/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    # 删除本地文件
    file_path = os.path.join(VIDEOS_DIR, video.video_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(video)
    db.commit()
    return {"msg": "Video deleted"}

# 3. 检测相关接口
@app.post("/api/detect/image")
async def detect_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # 预处理图像
    img = np.array(img)
    img = img.transpose(2, 0, 1)  # HWC to CHW
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # 推理
    pred = model(img, augment=False, visualize=False)
    
    # NMS
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
    
    detections = []
    for i, det in enumerate(pred):
        if len(det):
            # 将坐标从 img_size 缩放到 img0 大小
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img.shape).round()
            
            # 处理检测结果
            for *xyxy, conf, cls in reversed(det):
                detections.append({
                    "box": [round(x, 2) for x in xyxy],
                    "confidence": round(float(conf), 3),
                    "class": int(cls),
                    "class_name": model.names[int(cls)]
                })

    # 存储检测结果
    det_result = DetectionResult(video_id=None, result_json=str(detections), detected_at=datetime.utcnow())
    db.add(det_result)
    db.commit()
    db.refresh(det_result)
    return {"result_id": det_result.id, "detections": detections}

@app.post("/api/detect/video")
def detect_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="视频不存在")
    # 这里只做mock，实际应异步处理视频帧检测
    # 假设检测完毕，写入检测结果
    fake_result = [{"box": [0,0,100,100], "confidence": 0.9, "class": 0, "class_name": "floating_object"}]
    det_result = DetectionResult(video_id=video_id, result_json=str(fake_result), detected_at=datetime.utcnow())
    db.add(det_result)
    db.commit()
    db.refresh(det_result)
    video.status = "processed"
    db.commit()
    return {"result_id": det_result.id, "status": "processed"}

@app.get("/api/detection_results/{result_id}")
def get_detection_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(DetectionResult).filter(DetectionResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="检测结果不存在")
    return {
        "result_id": result.id,
        "video_id": result.video_id,
        "result_json": result.result_json,
        "detected_at": str(result.detected_at)
    }

@app.get("/api/detection_results/video/{video_id}")
def get_video_detection_results(video_id: int, db: Session = Depends(get_db)):
    results = db.query(DetectionResult).filter(DetectionResult.video_id == video_id).all()
    return [
        {"result_id": r.id, "result_json": r.result_json, "detected_at": str(r.detected_at)} for r in results
    ]

# 4. 日志相关接口
@app.get("/api/logs/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.user_id == user_id).all()
    return [
        {"id": l.id, "action": l.action, "action_time": str(l.action_time)} for l in logs
    ]

@app.post("/api/logs")
def add_log(user_id: int = Form(...), action: str = Form(...), db: Session = Depends(get_db)):
    log = Log(user_id=user_id, action=action, action_time=datetime.utcnow())
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"msg": "Log added", "log_id": log.id}

# 5. 系统相关接口
@app.get("/api/status")
def status():
    return {"status": "ok"}

@app.get("/api/system/info")
def system_info():
    import pkg_resources
    import time
    import platform
    import psutil
    import torch

    # 获取依赖包版本
    deps = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    # 获取服务器时间
    server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 获取系统信息
    system = platform.system()
    # 获取CPU使用率
    cpu_percent = psutil.cpu_percent()
    # 获取内存使用率
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    # 获取GPU信息（如果可用）
    gpu_info = "N/A"
    if torch.cuda.is_available():
        gpu_info = f"CUDA {torch.version.cuda}, Device: {torch.cuda.get_device_name(0)}"
    # 获取数据库连接状态（这里仅返回一个模拟状态）
    db_status = "Connected"

    return {
        "version": "1.0.0",
        "dependencies": deps,
        "server_time": server_time,
        "system": system,
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "gpu_info": gpu_info,
        "db_status": db_status
    } 