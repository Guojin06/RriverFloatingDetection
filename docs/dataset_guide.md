# 河流漂浮物检测系统 - 数据集配置指南

## 1. 数据集选择

### 1.1 推荐数据集
- COCO数据集
  - 下载地址：https://cocodataset.org/
  - 特点：包含大量物体检测图像，标注质量高
  - 适用场景：通用物体检测训练

- Open Images Dataset
  - 下载地址：https://storage.googleapis.com/openimages/web/index.html
  - 特点：大规模图像数据集，包含多种物体类别
  - 适用场景：大规模训练

- Roboflow Universe
  - 下载地址：https://universe.roboflow.com/
  - 特点：包含专门的河流漂浮物检测数据集
  - 适用场景：针对性训练

## 2. 开发环境配置

### 2.1 必需软件
- Python 3.8+
- VSCode
- Git
- MySQL

### 2.2 VSCode配置
1. 安装VSCode
2. 安装推荐扩展：
   - Python
   - Pylance
   - Python Docstring Generator
   - GitLens
   - MySQL

### 2.3 Python包安装
```bash
# 基础依赖
pip install torch torchvision
pip install opencv-python
pip install numpy

# Web框架
pip install fastapi
pip install uvicorn
pip install python-multipart

# 数据库
pip install mysql-connector-python
```

## 3. 数据集处理流程

### 3.1 数据预处理
1. 图像格式统一化
2. 图像大小调整
3. 数据增强
4. 标注格式转换

### 3.2 数据集划分
- 训练集：70%
- 验证集：15%
- 测试集：15%

### 3.3 数据存储结构
```
dataset/
├── train/
│   ├── images/
│   └── annotations/
├── val/
│   ├── images/
│   └── annotations/
└── test/
    ├── images/
    └── annotations/
```

## 4. 注意事项
1. 确保数据集标注质量
2. 定期备份数据集
3. 注意数据集的版权问题
4. 保持数据集版本管理 