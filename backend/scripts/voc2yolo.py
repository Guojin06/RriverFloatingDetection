import os
import xml.etree.ElementTree as ET
from shutil import copy2, rmtree

# VOC类别名（根据实际数据集修改）
CLASSES = [
    'bottle', 'milk-box', 'ball', 'plastic-bag', 'plastic-garbage', 'leaf', 'branch', 'grass'
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