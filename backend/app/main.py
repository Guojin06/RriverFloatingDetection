import sys
import os#os是python中的一个模块，用于操作文件和目录
YOLOV5_DIR = os.path.join(os.path.dirname(__file__), "../yolov5")
sys.path.append(YOLOV5_DIR)
sys.path.append(os.path.abspath(os.path.join(YOLOV5_DIR, "..")))  # 加入 backend 目录

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from PIL import Image
import torch
import io
import os
from config.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.models import User, Image as ImageModel, Log, DetectionResult
from fastapi.middleware.cors import CORSMiddleware
import shutil
from datetime import datetime
import numpy as np
from yolov5.utils.general import non_max_suppression, scale_boxes, check_img_size
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device
from fastapi.staticfiles import StaticFiles

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
MODEL_PATH ="runs/multi_class_run5/weights/best.pt"

# 使用 YOLOv5 官方推荐方式加载模型
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device

device = select_device('cpu')  # 或 'cuda:0' 如果有 GPU

if os.path.exists(MODEL_PATH):
    model = DetectMultiBackend(MODEL_PATH, device=device)
else:
    model = DetectMultiBackend(os.path.join(YOLOV5_DIR, 'yolov5s.pt'), device=device)

stride = int(model.stride)
imgsz = check_img_size(640, s=stride)  # 检查图片大小
model.warmup(imgsz=(1, 3, imgsz, imgsz))

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "../images")
os.makedirs(IMAGES_DIR, exist_ok=True)

app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

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
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):#Form是fastapi中的一个类，用于处理表单数据
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
    # 删除用户相关图片和日志
    db.query(ImageModel).filter(ImageModel.user_id == user_id).delete()
    db.query(Log).filter(Log.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}

# 图片相关接口
@app.post("/api/images/upload")
def upload_image(user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    filename = f"{user_id}_{file.filename}"
    save_path = os.path.join(IMAGES_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    image = ImageModel(user_id=user_id, image_path=filename, status="pending")
    db.add(image)
    db.commit()
    db.refresh(image)
    log = Log(user_id=user_id, action="upload_image", action_time=datetime.utcnow())#Log是app/models.py中的一个类，用于记录用户操作
    db.add(log)
    db.commit()
    return {"image_id": image.id, "image_path": filename, "status": image.status}

@app.get("/api/images/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    return {"image_id": image.id, "user_id": image.user_id, "image_path": image.image_path, "upload_time": str(image.upload_time), "status": image.status}

@app.get("/api/images/user/{user_id}")
def get_user_images(user_id: int, db: Session = Depends(get_db)):
    images = db.query(ImageModel).filter(ImageModel.user_id == user_id).all()
    return [{"image_id": img.id, "image_path": img.image_path, "upload_time": str(img.upload_time), "status": img.status} for img in images]

@app.delete("/api/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    file_path = os.path.join(IMAGES_DIR, image.image_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(image)
    db.commit()
    return {"msg": "Image deleted"}

# 检测相关接口
@app.post("/api/detect/image")
async def detect_image(image_id: int = Form(...), user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(img)
    img_tensor = img_np.transpose(2, 0, 1)  # HWC to CHW
    img_tensor = np.ascontiguousarray(img_tensor)
    img_tensor = torch.from_numpy(img_tensor).to(device)
    img_tensor = img_tensor.float()
    img_tensor /= 255.0
    if img_tensor.ndimension() == 3:
        img_tensor = img_tensor.unsqueeze(0)
    pred = model(img_tensor, augment=False, visualize=False)
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
    detections = []
    for i, det in enumerate(pred):
        if len(det):
            det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], img_tensor.shape).round()
            for *xyxy, conf, cls in reversed(det):
                detections.append({
                    "box": [round(float(x), 2) for x in xyxy],
                    "confidence": round(float(conf), 3),
                    "class": int(cls),
                    "class_name": model.names[int(cls)]
                })
    # 存储检测结果
    det_result = DetectionResult(image_id=image_id, result_json=str(detections), detected_at=datetime.utcnow())
    db.add(det_result)
    db.commit()
    db.refresh(det_result)
    # 写入日志
    log = Log(user_id=user_id, action="detect_image", action_time=datetime.utcnow())
    db.add(log)
    db.commit()
    return {"result_id": det_result.id, "detections": detections}

@app.get("/api/detection_results/{result_id}")
def get_detection_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(DetectionResult).filter(DetectionResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="检测结果不存在")
    return {
        "result_id": result.id,
        "image_id": result.image_id,
        "result_json": result.result_json,
        "detected_at": str(result.detected_at)
    }

@app.get("/api/detection_results/image/{image_id}")
def get_image_detection_results(image_id: int, db: Session = Depends(get_db)):
    results = db.query(DetectionResult).filter(DetectionResult.image_id == image_id).all()
    return [
        {"result_id": r.id, "image_id": r.image_id, "result_json": r.result_json, "detected_at": str(r.detected_at)} for r in results
    ]

# 4. 日志相关接口
@app.get("/api/logs/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.user_id == user_id).all()
    return [
        {"id": l.id, "user_id": l.user_id, "action": l.action, "action_time": str(l.action_time)} for l in logs
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