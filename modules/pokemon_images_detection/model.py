import os
import torch
import torch.nn as nn
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
from collections import Counter

def main():
    # 配置
    torch.manual_seed(42)
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "train_data")
    BATCH_SIZE = 32
    NUM_EPOCHS = 10
    NUM_WORKERS = 0  # macOS 推荐设为 0，防止 spawn 出错
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5]*3, std=[0.5]*3)
    ])

    train_dataset = datasets.ImageFolder(root=os.path.join(DATA_DIR, "train"), transform=transform)
    val_dataset = datasets.ImageFolder(root=os.path.join(DATA_DIR, "val"), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    class_counts = Counter(train_dataset.targets)
    idx_to_class = {v: k for k, v in train_dataset.class_to_idx.items()}
    for cls_idx, count in class_counts.items():
        print(f"类别 {idx_to_class[cls_idx]}：{count} 张图像")

    # 加载预训练 ResNet18 模型
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(train_dataset.classes))
    model = model.to(DEVICE)

    # 损失函数 & 优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    def evaluate(model, val_loader):
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
                outputs = model(imgs)
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)
        return correct / total if total > 0 else 0.0

    # 训练循环
    print("\n[INFO] Starting training...")
    for epoch in range(NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            outputs = model(imgs)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        acc = evaluate(model, val_loader)
        print(f"Epoch [{epoch+1}/{NUM_EPOCHS}] Loss: {running_loss/len(train_loader):.4f} | Val Acc: {acc*100:.2f}%")

    # 保存模型
    OUTPUT_DIR = os.path.join(BASE_DIR, "checkpoints")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    torch.save(model.state_dict(), OUTPUT_DIR + "/pokemon_resnet18.pth")
    print("\n[SUCCESS] Model saved to checkpoints/pokemon_resnet18.pth")

if __name__ == "__main__":
    main()