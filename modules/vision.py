import os
from modules.pokemon_images_detection.find_match import find_best_match, find_best_match_from_frame
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import time
from .chat import query_local

def describe_image(image_path: str) -> str:
    try:
        result = find_best_match(image_path, topk=1)

        if not result:
            return "❌ 无法识别图像中宝可梦。"
        
        matched_path, score = result[0]
        if score < 0.80:
            return f"❌ 匹配度仅为 {score:.2f}，未能识别出宝可梦。"

        matched_path, score = result[0]
        matched_name = os.path.basename(os.path.dirname(matched_path))
        print(f"[DEBUG] Matched Pokémon: {matched_name}, Score: {score:.4f}")

        # 查图鉴
        found, html = query_local(matched_name, "pokemon")
        if found:
            return f"✅ 与图像最相似的是：<b>{matched_name}</b>（相似度：{score:.2f}）<br>{html}"
        else:
            return f"⚠️ 找到最相似的宝可梦：<b>{matched_name}</b>（相似度：{score:.2f}），但未能查询到其图鉴信息。"
    
    except Exception as e:
        return f"❌ 识别图像时出错：{str(e)}"

class CameraCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("拍照识别宝可梦")
        self.setFixedSize(420, 400)

        self.video_label = QLabel("正在打开摄像头...", self)
        self.capture_button = QPushButton("📸 拍照识别", self)
        self.capture_button.clicked.connect(self.capture_image)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.capture_button)
        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.video_label.setText("❌ 无法打开摄像头")
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.captured_path = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        self.frame = frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        scaled = qt_image.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(QPixmap.fromImage(scaled))

    def capture_image(self):
        timestamp = int(time.time())
        path = f"captured_{timestamp}.jpg"
        cv2.imwrite(path, self.frame)
        self.captured_path = path
        self.accept()  # 关闭窗口并返回路径

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        self.timer.stop()
        event.accept()