# 河流漂浮物检测系统

基于 YOLOv5 和 FastAPI 的河流漂浮物智能检测系统。

## 项目结构

```
├── backend/                # 后端代码
│   ├── app/               # FastAPI 应用
│   ├── config/            # 配置文件
│   ├── dataset/           # 数据集目录
│   ├── scripts/           # 工具脚本
│   ├── tests/             # 测试代码
│   └── yolov5/            # YOLOv5 子模块
├── docs/                  # 项目文档
└── README.md             # 项目说明
```

## 环境要求

- Python 3.8+
- CUDA 11.0+ (GPU 训练需要)
- MySQL 8.0+

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/Guojin06/RriverFloatingDetection.git
cd RriverFloatingDetection
```

2. 安装依赖
```bash
# 创建虚拟环境
python -m venv env
source env/bin/activate  # Linux/Mac
# 或
.\env\Scripts\activate  # Windows

# 安装依赖
pip install -r backend/requirements.txt
```

3. 下载数据集
```bash
# 运行数据集下载脚本
python backend/scripts/download_dataset.py
```

4. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn app.main:app --reload
```

## 数据集说明

本项目使用的水面漂浮物数据集包含以下特点：
- 总图片数：2400 张
- 训练集：1920 张（80%）
- 验证集：240 张（10%）
- 测试集：240 张（10%）

数据集下载链接：[数据集下载地址]

## 模型训练

1. 准备数据集
```bash
# 运行数据预处理脚本
python backend/scripts/voc2yolo.py
```

2. 开始训练
```bash
cd backend/yolov5
python train.py --img 640 --batch 16 --epochs 100 --data ../config/dataset.yaml --weights yolov5s.pt
```

## API 文档

启动服务后访问：http://localhost:8000/docs

主要接口：
- POST /api/detect：图像检测
- GET /api/status：系统状态
- POST /api/batch：批量检测

## 开发文档

详细文档请参考：
- [环境配置与数据集准备](docs/blog_tutorial.md)
- [模型训练与评估](docs/blog_tutorial.md#从零开始搭建河流漂浮物检测系统二模型训练与评估)
- [API开发与系统集成](docs/blog_tutorial.md#从零开始搭建河流漂浮物检测系统三api开发与系统集成)

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 作者：郭金
- 邮箱：your.email@example.com
- GitHub：[Guojin06](https://github.com/Guojin06) 