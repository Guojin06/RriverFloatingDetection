import os
import requests
import zipfile
from pathlib import Path
import shutil
from tqdm import tqdm

def download_file(url, save_path):
    """下载文件"""
    print(f"正在下载: {url}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(save_path, 'wb') as f:
        if total_size == 0:
            f.write(response.content)
        else:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc='下载进度') as pbar:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    pbar.update(len(data))
    print("下载完成！")

def prepare_dataset():
    """准备数据集"""
    # 创建数据集目录
    base_dir = Path("dataset")
    raw_dir = base_dir / "raw"
    processed_dir = base_dir / "processed"
    
    # 创建必要的目录
    for dir_path in [raw_dir, processed_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # 数据集URL（Roboflow Universe上的河流漂浮物数据集）
    dataset_url = "https://universe.roboflow.com/ds/your-dataset-url"  # 需要替换为实际的URL
    
    # 临时使用示例数据集
    print("由于示例数据集URL未设置，我们将创建一个示例数据集...")
    
    # 创建示例图像和标注
    for split in ['train', 'val', 'test']:
        # 创建示例图像
        img_dir = processed_dir / split / "images"
        label_dir = processed_dir / split / "labels"
        img_dir.mkdir(parents=True, exist_ok=True)
        label_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建示例标注文件
        for i in range(5):  # 每个集合创建5个示例文件
            # 创建示例标注
            label_path = label_dir / f"image_{i}.txt"
            with open(label_path, 'w') as f:
                # 示例标注：类别0，中心点(0.5, 0.5)，宽高(0.2, 0.2)
                f.write("0 0.5 0.5 0.2 0.2\n")
            
            print(f"创建示例文件: {label_path}")
    
    print("\n示例数据集创建完成！")
    print("\n要使用实际数据集，请：")
    print("1. 访问 https://universe.roboflow.com/roboflow-universe-projects/river-floating-objects")
    print("2. 下载数据集（需要注册Roboflow账号）")
    print("3. 解压下载的文件到 dataset/raw 目录")
    print("4. 运行数据预处理脚本（将在下一篇教程中提供）")
    print("\n数据集目录结构：")
    print(f"- 训练集图像: {processed_dir}/train/images")
    print(f"- 验证集图像: {processed_dir}/val/images")
    print(f"- 测试集图像: {processed_dir}/test/images")
    print("\n对应的标注文件应放在labels目录中，格式为YOLO格式（.txt文件）")

if __name__ == "__main__":
    prepare_dataset() 