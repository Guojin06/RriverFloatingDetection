import os
import requests
from tqdm import tqdm
import zipfile
import shutil

def download_file(url, filename):
    """下载文件并显示进度条"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def setup_dataset():
    """设置数据集目录结构"""
    # 创建必要的目录
    dirs = [
        'backend/dataset/raw',
        'backend/dataset/processed',
        'backend/dataset/processed/train/images',
        'backend/dataset/processed/train/labels',
        'backend/dataset/processed/val/images',
        'backend/dataset/processed/val/labels',
        'backend/dataset/processed/test/images',
        'backend/dataset/processed/test/labels'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def main():
    """主函数"""
    print("开始设置数据集...")
    
    # 创建目录结构
    setup_dataset()
    
    # 数据集下载链接（这里需要替换为实际的数据集下载链接）
    dataset_url = "YOUR_DATASET_DOWNLOAD_URL"
    dataset_zip = "backend/dataset/raw/dataset.zip"
    
    if not os.path.exists(dataset_zip):
        print(f"下载数据集...")
        download_file(dataset_url, dataset_zip)
    
    # 解压数据集
    if os.path.exists(dataset_zip):
        print("解压数据集...")
        with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
            zip_ref.extractall("backend/dataset/raw")
        
        # 删除zip文件
        os.remove(dataset_zip)
    
    print("数据集设置完成！")
    print("\n请确保：")
    print("1. 数据集已正确解压到 backend/dataset/raw 目录")
    print("2. 运行 voc2yolo.py 脚本将数据集转换为YOLO格式")
    print("3. 检查 dataset.yaml 配置文件是否正确")

if __name__ == "__main__":
    main() 