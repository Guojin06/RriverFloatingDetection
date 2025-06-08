# 河流漂浮物检测系统 API 接口文档

## 1. 用户相关接口

### 1.1 用户注册
- **接口**：POST /api/register
- **作用**：注册新用户
- **请求体**：
```json
{
  "username": "testuser",
  "password": "123456"
}
```
- **响应**：
```json
{
  "user_id": 1,
  "username": "testuser",
  "role": "user"
}
```

### 1.2 用户登录
- **接口**：POST /api/login
- **作用**：用户登录，返回 token
- **请求体**：
```json
{
  "username": "testuser",
  "password": "123456"
}
```
- **响应**：
```json
{
  "user_id": 1,
  "token": "xxxxxx"
}
```

### 1.3 获取用户信息
- **接口**：GET /api/users/{user_id}
- **作用**：获取指定用户信息
- **响应**：
```json
{
  "user_id": 1,
  "username": "testuser",
  "role": "user",
  "created_at": "2024-06-05T12:00:00"
}
```

### 1.4 修改用户信息
- **接口**：PUT /api/users/{user_id}
- **作用**：修改用户信息
- **请求体**：
```json
{
  "username": "newname",
  "password": "newpass",
  "role": "admin"
}
```
- **响应**：同上

### 1.5 删除用户
- **接口**：DELETE /api/users/{user_id}
- **作用**：删除用户
- **响应**：
```json
{"msg": "User deleted"}
```

---

## 2. 视频相关接口

### 2.1 上传视频
- **接口**：POST /api/videos/upload
- **作用**：上传视频文件，返回视频ID
- **请求参数**：form-data: file=xxx.mp4, user_id=1
- **响应**：
```json
{
  "video_id": 10,
  "video_path": "videos/xxx.mp4",
  "status": "pending"
}
```

### 2.2 获取视频信息
- **接口**：GET /api/videos/{video_id}
- **作用**：获取指定视频信息
- **响应**：
```json
{
  "video_id": 10,
  "user_id": 1,
  "video_path": "videos/xxx.mp4",
  "upload_time": "2024-06-05T12:00:00",
  "status": "pending"
}
```

### 2.3 获取用户所有视频
- **接口**：GET /api/videos/user/{user_id}
- **作用**：获取某用户所有视频
- **响应**：
```json
[
  {"video_id": 10, "video_path": "videos/xxx.mp4", ...},
  {"video_id": 11, "video_path": "videos/yyy.mp4", ...}
]
```

### 2.4 删除视频
- **接口**：DELETE /api/videos/{video_id}
- **作用**：删除指定视频
- **响应**：
```json
{"msg": "Video deleted"}
```

---

## 3. 检测相关接口

### 3.1 单张图片检测
- **接口**：POST /api/detect/image
- **作用**：上传图片，返回检测结果（不入库）
- **请求参数**：form-data: file=xxx.jpg
- **响应**：
```json
{
  "detections": [
    {"box": [x1, y1, x2, y2], "confidence": 0.98, "class": 0, "class_name": "floating_object"}
  ]
}
```

### 3.2 视频检测任务
- **接口**：POST /api/detect/video
- **作用**：对已上传视频发起检测任务，返回检测结果ID
- **请求体**：
```json
{
  "video_id": 10
}
```
- **响应**：
```json
{
  "result_id": 100,
  "status": "processing"
}
```

### 3.3 查询检测结果详情
- **接口**：GET /api/detection_results/{result_id}
- **作用**：获取检测结果详情
- **响应**：
```json
{
  "result_id": 100,
  "video_id": 10,
  "result_json": {...},
  "detected_at": "2024-06-05T12:00:00"
}
```

### 3.4 查询某视频所有检测结果
- **接口**：GET /api/detection_results/video/{video_id}
- **作用**：获取某视频的所有检测结果
- **响应**：
```json
[
  {"result_id": 100, "result_json": {...}, ...},
  {"result_id": 101, "result_json": {...}, ...}
]
```

---

## 4. 日志相关接口

### 4.1 查询用户操作日志
- **接口**：GET /api/logs/user/{user_id}
- **作用**：获取用户操作日志
- **响应**：
```json
[
  {"id": 1, "action": "login", "action_time": "..."},
  {"id": 2, "action": "upload_video", "action_time": "..."}
]
```

### 4.2 新增操作日志
- **接口**：POST /api/logs
- **作用**：记录操作日志
- **请求体**：
```json
{
  "user_id": 1,
  "action": "upload_video"
}
```
- **响应**：
```json
{"msg": "Log added"}
```

---

## 5. 系统相关接口

### 5.1 系统健康检查
- **接口**：GET /api/status
- **作用**：检查系统运行状态
- **响应**：
```json
{"status": "ok"}
```

---

> 所有接口均返回标准 JSON 格式，出错时返回 `{"error": "错误信息"}`。
> 文件上传接口请使用 form-data 格式。
> 详细参数说明和示例见 Swagger UI。 