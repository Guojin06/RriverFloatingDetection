# 基于深度学习的河道漂浮物检测系统

## 项目简介
本项目旨在开发一个基于深度学习的河道漂浮物检测系统，实现对河道视频流中的漂浮物自动检测、分类与定位，并通过Web界面进行展示和管理。

## 技术栈
- **后端**：FastAPI（Python 3.8+）
- **前端**：HTML + JavaScript（可后续引入Vue/React等）
- **数据库**：MySQL 8.0.42
- **数据库可视化**：HeidiSQL
- **深度学习**：PyTorch/TensorFlow（可选，建议先用预训练模型）

## 训练集规模与训练建议
- 总图片数：2400 张
- 训练集：1920 张（80%）
- 验证集：240 张（10%）
- 测试集：240 张（10%）
- 推荐训练轮次（epochs）：100 轮（调试可用 5~20 轮）
- 推荐 batch size：8~16
- 训练时间：
  - CPU 约 6~12 小时
  - GPU（如 RTX 3050 Ti）约 30~60 分钟

## 目录结构
```
river-floating-object-detection/
│
├── backend/                # FastAPI后端
│   ├── app/
│   │   ├── main.py         # FastAPI入口
│   │   ├── api/            # 路由
│   │   ├── models/         # Pydantic模型
│   │   ├── crud/           # 数据库操作
│   │   ├── core/           # 配置、工具
│   │   └── ml/             # 深度学习相关代码
│   └── requirements.txt    # 后端依赖
│
├── frontend/               # 前端
│   ├── static/             # 静态资源
│   ├── templates/          # HTML模板
│   └── app.js              # 前端逻辑
│
├── db/                     # 数据库相关
│   ├── schema.sql          # 数据库表结构
│   └── init.sql            # 初始化脚本
│
├── docs/                   # 文档
│   └── README.md           # 项目说明
│
└── .gitignore
```

## 开发计划
1. **第一阶段**（1-2天）：需求分析、项目框架搭建、基础联通
2. **第二阶段**（3-12天）：模型集成、API开发、前端初步实现、数据库设计
3. **第三阶段**（13-15天）：系统优化、前端完善、文档与演示

## 当前具体实施计划
### 第一阶段（当前进行中，1-2天）
- 明确需求和功能模块（如：用户管理、视频上传/流、检测结果展示、数据存储等）
- 搭建项目基础框架（前后端、数据库初始化）
- 完成最基础的"Hello World"级联通（前端能访问后端，后端能操作数据库）

#### 具体分工建议
- 组员A：负责后端FastAPI框架搭建，数据库连接测试
- 组员B：负责前端HTML页面初步搭建，与后端接口联通测试
- 组员C：负责MySQL数据库安装、表结构初步设计、HeidiSQL可视化配置

### 第二阶段（3-12天）
- 深度学习模型选型、训练与集成（可先用预训练模型做demo）
- 完善后端API（如：上传视频、获取检测结果、用户管理等）
- 前端初步页面开发（如：登录、上传、结果展示）
- 数据库表结构设计与实现
- 前后端联调，能跑通一个完整流程

### 第三阶段（13-15天）
- 优化模型与系统性能
- 完善前端交互与美化
- 增加日志、异常处理、权限等
- 项目文档、部署、演示准备

## 快速开始

### 1. 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. 前端启动
直接用浏览器打开 `frontend/templates/index.html`，或用简单的HTTP服务器（如Python的http.server）。

### 3. 数据库
- 安装MySQL 8.0.42
- 用HeidiSQL导入 `db/schema.sql` 初始化表结构

## 贡献说明
- 代码规范：PEP8
- 分支管理：feature/xxx
- 提交信息：简明扼要

## 联系方式
- 组员A
- 组员B
- 组员C 

## 如何用训练好的模型推理

```python
import torch

# 加载训练好的模型权重
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/river_floating_detection/weights/best.pt', source='local')

# 对单张图片进行推理
results = model('test.jpg')

# 显示检测结果
results.show()

# 保存检测结果
results.save('output/')
```

## 目录结构说明
- backend/app/：FastAPI 主应用及路由、模型、数据库操作等
- backend/yolov5/：YOLOv5 源码及训练、推理脚本
- backend/dataset/：数据集目录，含原始和处理后数据
- backend/scripts/：数据处理、格式转换等脚本
- backend/config/：配置文件（如训练参数、数据库配置）
- backend/runs/：训练输出目录，含权重、日志、可视化结果
- docs/：项目文档、博客、数据集说明等

## 常见问题与解决方案

### 1. 训练太慢或显存不足
- 降低 batch size 或图片分辨率
- 使用更轻量的模型（如 yolov5n、yolov5s）

### 2. GPU 未被检测到
- 检查 CUDA 驱动和 torch 安装
- 使用 `torch.cuda.is_available()` 检查 GPU

### 3. 依赖冲突或安装失败
- 建议使用虚拟环境
- 遇到网络超时可用清华镜像

### 4. 数据集路径报错
- 检查 dataset.yaml 的 path 字段是否为绝对路径
- train/val 路径为相对路径，如 train: train/images

### 5. 标签文件为空
- 检查 VOC->YOLO 转换脚本类别名是否与数据集一致 

# 常见错误与解决手册（2024-06-05 晚）

## 1. 数据库连接失败
- **报错现象**：`Access denied for user ...` 或 `数据库连接失败！`
- **常见原因**：
  - 用户名/密码错误
  - 用户没有远程访问权限
  - 数据库主机、端口配置错误
- **解决方法**：
  1. 检查 `.env` 文件或 `config/database.py`，确保用户名、密码、主机、端口正确。
  2. 用 HeidiSQL 等工具确认远程能连上。
  3. 如需远程访问，MySQL 用户需授权：
     ```sql
     GRANT ALL PRIVILEGES ON 数据库名.* TO '用户名'@'%' IDENTIFIED BY '密码';
     FLUSH PRIVILEGES;
     ```
  4. 若密码被环境变量覆盖，优先以 `.env` 文件为准，或直接在代码里写死调试。

## 2. cryptography 包安装失败/进程占用
- **报错现象**：`WinError 32`、`cryptography package is required for sha256_password...`、pip 安装卡死
- **常见原因**：
  - pip 临时文件被杀毒/系统占用
  - 认证方式为 caching_sha2_password
- **解决方法**：
  1. 彻底关闭所有 Python/IDE/资源管理器/杀毒软件
  2. 清空 `C:\Users\用户名\AppData\Local\Temp` 和 pip 缓存
  3. 用管理员权限 PowerShell，设置临时目录：
     ```powershell
     $env:TEMP = "D:\piptemp"
     $env:TMP = "D:\piptemp"
     pip install cryptography --no-cache-dir
     ```
  4. **推荐**：将 MySQL 用户认证方式改为 mysql_native_password，避免依赖 cryptography：
     ```sql
     ALTER USER '用户名'@'%' IDENTIFIED WITH mysql_native_password BY '密码';
     FLUSH PRIVILEGES;
     ```

## 3. FastAPI Swagger UI `Failed to fetch`/CORS 问题
- **报错现象**：Swagger UI 调用接口报 `Failed to fetch`，提示 CORS/Network Failure
- **解决方法**：
  1. 在 `main.py` 添加 CORS 中间件：
     ```python
     from fastapi.middleware.cors import CORSMiddleware
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["*"],
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )
     ```
  2. 重启 FastAPI 服务，刷新 Swagger 页面

## 4. 环境变量/配置优先级混乱
- **现象**：实际连接信息与预期不符
- **解决方法**：
  1. 优先检查 `.env` 文件内容
  2. 检查系统环境变量（PowerShell 用 `$env:MYSQL_PASSWORD` 查看）
  3. 代码调试时可直接写死参数

## 5. Python 包导入失败（如 `ModuleNotFoundError: No module named 'config'`）
- **解决方法**：
  - 在脚本开头加：
    ```python
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ```

---

如遇到其他问题，建议：
- 先用最小脚本测试数据库连接
- 逐步排查环境变量、依赖、端口、网络
- 记录每一步的报错和日志，便于定位 