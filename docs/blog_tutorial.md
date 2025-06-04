# 从零开始搭建河流漂浮物检测系统（一）：环境配置与数据集准备

> 本教程将带领大家从零开始搭建一个河流漂浮物检测系统。我们将使用Python、PyTorch和FastAPI来构建这个系统。本系列教程适合有一定Python基础的开发者，我们将一步一步详细讲解每个环节。

## 目录
- [一、开发环境配置](#一开发环境配置)
  - [1. Python环境](#1-python环境)
  - [2. 项目依赖](#2-项目依赖)
  - [3. 数据库配置](#3-数据库配置)
- [二、数据集准备](#二数据集准备)
  - [1. 数据集选择与下载](#1-数据集选择与下载)
  - [2. 数据集原始目录结构](#2-数据集原始目录结构)
  - [3. VOC格式转YOLO格式及自动整理](#3-voc格式转yolo格式及自动整理)
  - [4. 数据集格式说明](#4-数据集格式说明)
  - [5. 数据集验证](#5-数据集验证)
- [三、下一步计划](#三下一步计划)
- [四、参考资源](#四参考资源)

## 一、开发环境配置

### 1. Python环境
- 使用Python 3.12.9
- 已创建虚拟环境：`env`
- 使用Cursor IDE进行开发

### 2. 项目依赖
在 `backend/requirements.txt` 中配置：
```bash
# 基础依赖
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0
numpy>=1.24.0

# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0
python-multipart>=0.0.6

# 数据库
mysql-connector-python>=8.0.0
SQLAlchemy>=2.0.0
alembic>=1.12.0
pymysql>=1.1.0

# 工具包
python-dotenv>=1.0.0
pydantic>=2.0.0

# 数据集处理
requests>=2.31.0
tqdm>=4.66.0
Pillow>=10.0.0
```

### 3. 数据库配置
- 使用MySQL 8.0.42
- 数据库名称：river_floating_detection
- 使用HeidiSQL进行数据库管理

## 二、数据集准备

### 1. 数据集选择与下载
本项目选用公开的水面漂浮物VOC格式数据集（如"水面漂浮物数据集-2400"），下载后解压到 `backend/dataset/raw/水面漂浮物数据集-2400/`。

### 2. 数据集原始目录结构
```
dataset/
├── raw/
│   └── 水面漂浮物数据集-2400/
│       └── VOCdevkit/
│           └── VOC2007/
│               ├── JPEGImages/        # 原始图片
│               ├── Annotations/       # VOC XML标注
│               ├── ImageSets/
│               │   └── Main/          # train/val/test划分
```

### 3. VOC格式转YOLO格式及自动整理

VOC格式不能直接用于YOLO训练，需要转换为YOLO格式。我们提供自动转换脚本：

**脚本路径：`backend/scripts/voc2yolo.py`**

```python
import os
import xml.etree.ElementTree as ET
from shutil import copy2, rmtree

# VOC类别名（请根据实际数据集修改）
CLASSES = [
    "floating_object"
]

# 路径配置
VOC_ROOT = os.path.join(os.path.dirname(__file__), '../dataset/raw/水面漂浮物数据集-2400/VOCdevkit/VOC2007')
PROCESSED_ROOT = os.path.join(os.path.dirname(__file__), '../dataset/processed')

IMAGE_DIR = os.path.join(VOC_ROOT, 'JPEGImages')
ANNOTATION_DIR = os.path.join(VOC_ROOT, 'Annotations')
IMAGESETS_DIR = os.path.join(VOC_ROOT, 'ImageSets/Main')

SPLITS = ['train', 'val', 'test']

# 清理旧目录
def clean_dir(path):
    if os.path.exists(path):
        rmtree(path)
    os.makedirs(path)

def convert_bbox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_path, yolo_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    with open(yolo_path, 'w', encoding='utf-8') as out_file:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in CLASSES:
                continue
            cls_id = CLASSES.index(cls)
            xmlbox = obj.find('bndbox')
            b = [float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]
            bbox = convert_bbox((w, h), b)
            out_file.write(f"{cls_id} {' '.join([str(round(a, 6)) for a in bbox])}\n")

def process_split(split):
    imgset_path = os.path.join(IMAGESETS_DIR, f'{split}.txt')
    with open(imgset_path, 'r') as f:
        img_ids = [x.strip() for x in f.readlines()]
    img_out_dir = os.path.join(PROCESSED_ROOT, split, 'images')
    label_out_dir = os.path.join(PROCESSED_ROOT, split, 'labels')
    clean_dir(img_out_dir)
    clean_dir(label_out_dir)
    for img_id in img_ids:
        img_file = os.path.join(IMAGE_DIR, f'{img_id}.jpg')
        xml_file = os.path.join(ANNOTATION_DIR, f'{img_id}.xml')
        yolo_file = os.path.join(label_out_dir, f'{img_id}.txt')
        if os.path.exists(img_file) and os.path.exists(xml_file):
            copy2(img_file, img_out_dir)
            convert_annotation(xml_file, yolo_file)

if __name__ == '__main__':
    for split in SPLITS:
        print(f'Processing {split} set...')
        process_split(split)
    print('VOC to YOLO conversion done!')

### 4. 数据集格式说明
- 图像格式：JPG/PNG
- 标注格式：YOLO格式（.txt文件）
  - 每行格式：`class_id x_center y_center width height`
  - 所有值都是归一化的（0-1之间）
  - 示例：
    ```
    0 0.5 0.5 0.2 0.2  # 类别0，中心点(0.5, 0.5)，宽高(0.2, 0.2)
    ```

### 5. 数据集验证
1. 检查图像完整性
2. 验证标注文件
3. 确保训练集/验证集/测试集划分合理

## 三、下一步计划

1. 数据预处理和增强
2. 模型训练和评估
3. 模型部署和优化

## 四、参考资源

1. [YOLOv5官方文档](https://github.com/ultralytics/yolov5)
2. [Roboflow Universe](https://universe.roboflow.com/)
3. [OpenCV-Python教程](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

---

> 下一篇我们将详细介绍数据预处理和模型训练的具体实现，敬请期待！

# 从零开始搭建河流漂浮物检测系统（二）：模型训练与评估

## 目录
- [一、模型训练准备](#一模型训练准备)
  - [1. 数据集配置](#1-数据集配置)
  - [2. 训练参数设置](#2-训练参数设置)
  - [3. 预训练模型选择](#3-预训练模型选择)
- [二、模型训练过程](#二模型训练过程)
  - [1. 训练脚本说明](#1-训练脚本说明)
  - [2. 训练过程监控](#2-训练过程监控)
  - [3. 模型评估指标](#3-模型评估指标)
- [三、模型优化与验证](#三模型优化与验证)
  - [1. 模型性能优化](#1-模型性能优化)
  - [2. 模型验证测试](#2-模型验证测试)
  - [3. 模型导出部署](#3-模型导出部署)
- [四、下一步计划](#四下一步计划)
- [五、参考资源](#五参考资源)

## 一、模型训练准备

### 训练集规模与轮次
- **总图片数**：2400 张
- **训练集**：1920 张（80%）
- **验证集**：240 张（10%）
- **测试集**：240 张（10%）
- **训练轮次（epochs）**：常用 100 轮，调试时可用 5~20 轮
- **批次大小（batch size）**：推荐 8~16（受限于 GPU 显存）

### 训练时间估算
- **CPU 训练**：100 轮大约需要 6~12 小时（取决于 CPU 性能）
- **GPU 训练（如 RTX 3050 Ti）**：100 轮大约 30~60 分钟，5 轮只需几分钟
- **影响因素**：图片数量、分辨率、batch size、数据增强、显卡性能

### 1. 数据集配置
- 使用已转换的YOLO格式数据集
- 配置数据集YAML文件
- 设置训练集、验证集和测试集路径

#### 数据集配置文件 (dataset.yaml)
```yaml
# 河流漂浮物检测数据集配置
path: ../dataset/processed  # 数据集根目录
train: train/images  # 训练集图片相对路径
val: val/images      # 验证集图片相对路径
test: test/images    # 测试集图片相对路径

# 类别信息
nc: 1  # 类别数量
names: ['floating_object']  # 类别名称
```

### 2. 训练参数设置
- 基础配置：
  - 图像尺寸：640x640
  - 批次大小：16
  - 训练轮数：100
  - 学习率：0.01
  - 权重衰减：0.0005
  - 动量：0.937

- 数据增强策略：
  - 随机水平翻转
  - 随机缩放
  - 随机亮度、对比度调整
  - Mosaic增强
  - 随机裁剪

### 3. 预训练模型选择
- 选择YOLOv5s作为基础模型
  - 模型大小：7.2MB
  - 参数量：7.0M
  - 适合部署在普通服务器
  - 在速度和精度之间取得良好平衡

#### 模型下载
```bash
# 下载预训练模型
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
```

## 二、模型训练过程

### 1. 训练脚本说明

```mermaid
flowchart TD
    A[启动 train.py] --> B[加载配置和超参数]
    B --> C[加载数据集]
    C --> D[构建模型并加载预训练权重]
    D --> E[初始化优化器和损失函数]
    E --> F{进入训练循环 (每个 epoch)}
    F --> G[训练: 前向传播、反向传播、参数更新]
    G --> H[记录训练损失、可视化样本]
    H --> I[验证: 在验证集上评估]
    I --> J[记录验证损失和指标]
    J --> K[保存权重和日志文件]
    K --> L{是否达到最大 epoch?}
    L -- 否 --> F
    L -- 是 --> M[训练结束，保存最终模型和日志]
    M --> N[可选: 启动 TensorBoard 查看曲线]
```

### 2. 训练过程监控
- 使用TensorBoard监控训练过程：
```bash
# 启动TensorBoard
tensorboard --logdir runs/train
```

- 监控指标：
  - 训练损失（train_loss）
  - 验证损失（val_loss）
  - mAP@0.5
  - mAP@0.5:0.95
  - 精确率（Precision）
  - 召回率（Recall）

### 3. 模型评估指标
- 主要评估指标：
  - mAP@0.5: 在IoU=0.5时的平均精度
  - mAP@0.5:0.95: 在IoU=0.5~0.95范围内的平均精度
  - 精确率（Precision）：正确检测的物体占所有检测结果的比例
  - 召回率（Recall）：正确检测的物体占所有真实物体的比例
  - F1分数：精确率和召回率的调和平均数

## 三、模型优化与验证

### 1. 模型性能优化
- 超参数调优策略：
  1. 学习率调整
     - 初始学习率：0.01
     - 使用余弦退火调度器
     - 最小学习率：0.0001
  
  2. 数据增强调整
     - 根据验证集性能调整增强强度
     - 考虑添加特定场景的增强方法
  
  3. 模型结构优化
     - 根据实际检测效果调整网络层数
     - 考虑使用更轻量级的backbone

### 2. 模型验证测试
- 测试流程：
  1. 在测试集上评估模型性能
  2. 进行实际场景测试
     - 不同光照条件
     - 不同天气条件
     - 不同拍摄角度
  3. 分析模型优缺点
     - 检测速度
     - 检测精度
     - 误检和漏检情况

### 3. 模型导出部署
- 导出格式：
  1. ONNX格式（用于跨平台部署）
  2. TorchScript格式（用于PyTorch部署）
  3. CoreML格式（用于iOS部署）
  4. TensorRT格式（用于NVIDIA GPU加速）

- 优化方法：
  1. 模型量化（INT8/FP16）
  2. 模型剪枝
  3. 知识蒸馏

## 四、下一步计划

1. 开发RESTful API接口
   - 图像上传接口
   - 检测结果返回接口
   - 批量处理接口

2. 系统集成
   - 前后端对接
   - 数据库集成
   - 用户认证系统

3. 系统部署
   - 服务器环境配置
   - 性能优化
   - 监控系统搭建

## 五、参考资源

1. [YOLOv5训练指南](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data)
2. [PyTorch文档](https://pytorch.org/docs/stable/index.html)
3. [FastAPI文档](https://fastapi.tiangolo.com/)
4. [项目GitHub仓库](https://github.com/Guojin06/RriverFloatingDetection.git)

---

> 下一篇我们将详细介绍API开发的具体实现，包括RESTful接口设计、数据库集成等内容，敬请期待！

# 从零开始搭建河流漂浮物检测系统（三）：API开发与系统集成

## 目录
- [一、API设计](#一api设计)
  - [1. 接口规划](#1-接口规划)
  - [2. 数据模型设计](#2-数据模型设计)
  - [3. 认证与授权](#3-认证与授权)
- [二、后端开发](#二后端开发)
  - [1. FastAPI框架搭建](#1-fastapi框架搭建)
  - [2. 数据库集成](#2-数据库集成)
  - [3. 模型集成](#3-模型集成)
- [三、系统集成](#三系统集成)
  - [1. 前后端对接](#1-前后端对接)
  - [2. 文件存储系统](#2-文件存储系统)
  - [3. 日志系统](#3-日志系统)
- [四、系统测试](#四系统测试)
  - [1. 单元测试](#1-单元测试)
  - [2. 接口测试](#2-接口测试)
  - [3. 性能测试](#3-性能测试)
- [五、部署准备](#五部署准备)
  - [1. 环境配置](#1-环境配置)
  - [2. 容器化部署](#2-容器化部署)
  - [3. 监控系统](#3-监控系统)
- [六、参考资源](#六参考资源)

## 一、API设计

### 1. 接口规划
- 图像上传接口
- 检测结果返回接口
- 批量处理接口

### 2. 数据模型设计
- 设计数据模型，包括输入和输出格式

### 3. 认证与授权
- 实现用户认证和权限管理

## 二、后端开发

### 1. FastAPI框架搭建
- 创建FastAPI项目结构
- 定义路由和处理逻辑

### 2. 数据库集成
- 连接数据库，实现数据存储和查询

### 3. 模型集成
- 加载训练好的模型，实现推理功能

## 三、系统集成

### 1. 前后端对接
- 实现前后端通信，确保数据交互

### 2. 文件存储系统
- 实现文件上传和存储功能

### 3. 日志系统
- 实现日志记录和分析功能

## 四、系统测试

### 1. 单元测试
- 编写单元测试，确保代码质量

### 2. 接口测试
- 使用工具或脚本，测试API接口功能

### 3. 性能测试
- 使用工具或脚本，测试API性能指标

## 五、部署准备

### 1. 环境配置
- 配置服务器环境，确保系统运行

### 2. 容器化部署
- 使用容器技术，实现系统部署

### 3. 监控系统
- 实现系统监控和告警功能

## 六、参考资源

1. [YOLOv5训练指南](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data)
2. [PyTorch文档](https://pytorch.org/docs/stable/index.html)
3. [FastAPI文档](https://fastapi.tiangolo.com/)
4. [项目GitHub仓库](https://github.com/Guojin06/RriverFloatingDetection.git)

## 四、目录结构详细解释

- `backend/app/`：FastAPI 主应用及路由、模型、数据库操作等
- `backend/yolov5/`：YOLOv5 源码及训练、推理脚本
- `backend/dataset/`：数据集目录，含原始和处理后数据
- `backend/scripts/`：数据处理、格式转换等脚本
- `backend/config/`：配置文件（如训练参数、数据库配置）
- `backend/runs/`：训练输出目录，含权重、日志、可视化结果
- `docs/`：项目文档、博客、数据集说明等

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

---

> 下一篇我们将详细介绍API开发的具体实现，包括RESTful接口设计、数据库集成等内容，敬请期待！ 