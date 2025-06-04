import os#os模块用于获取环境变量
from pathlib import Path#pathlib模块用于处理文件路径

def create_dataset_directories():#创建数据集目录结构，def是定义函数的关键字
    """创建数据集目录结构"""
    # 定义基础目录
    base_dir = Path("dataset")
    
    # 定义需要创建的目录
    directories = [
        "raw/images",
        "raw/annotations",
        "processed/train/images",
        "processed/train/labels",
        "processed/val/images",
        "processed/val/labels",
        "processed/test/images",
        "processed/test/labels",
        "models/checkpoints",
        "models/best"
    ]#需要创建的目录列表
    
    # 创建目录
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {full_path}")

if __name__ == "__main__":
    create_dataset_directories() 