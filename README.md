# 基于深度学习的河道漂浮物检测系统

## 项目简介
本项目旨在开发一个基于深度学习的河道漂浮物检测系统，实现对河道视频流中的漂浮物自动检测、分类与定位，并通过Web界面进行展示和管理。

## 技术栈
- **后端**：FastAPI（Python 3.8+）
- **前端**：HTML + JavaScript（可后续引入Vue/React等）
- **数据库**：MySQL 8.0.42
- **数据库可视化**：HeidiSQL
- **深度学习**：PyTorch/TensorFlow（可选，建议先用预训练模型）

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