import os

labels_dir = 'dataset/processed/train/labels'
all_classes = set()
for fname in os.listdir(labels_dir):
    if not fname.endswith('.txt'):
        continue
    with open(os.path.join(labels_dir, fname), 'r') as f:
        for line in f:
            if line.strip():
                class_id = line.strip().split()[0]
                all_classes.add(class_id)

print('标签中出现的类别编号:', all_classes)
print('类别数量:', len(all_classes))