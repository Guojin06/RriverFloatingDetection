import os
import xml.etree.ElementTree as ET

xml_dir = 'dataset/raw/水面漂浮物数据集-2400/VOCdevkit/VOC2007/Annotations'
all_classes = set()

for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith('.xml'):
        continue
    tree = ET.parse(os.path.join(xml_dir, xml_file))
    root = tree.getroot()
    for obj in root.findall('object'):
        name = obj.find('name').text
        all_classes.add(name)

print('所有类别:', all_classes)