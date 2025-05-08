import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextBrowser, QLineEdit, QPushButton, QLabel, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# 让你可以导入 modules 目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.chat import ask_gpt
from modules.vision import describe_image


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("洛托姆助手")
        self.setFixedSize(480, 720)

        # === 背景图 ===
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assets/rotom_bg (1).png").scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()

        # === 聊天框 ===
        self.chat_display = QTextBrowser(self)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Arial';
            }
        """)

        # === 输入框 ===
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("ロトムに話しかけてみよう")
        self.input_box.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                font-size: 14px;
            }
        """)

        # === 发送按钮 ===
        self.send_button = QPushButton("发送")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;
                color: white;
                border-radius: 15px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF7373;
            }
        """)

        # === 上传按钮 ===
        self.upload_button = QPushButton("📷 图片上传")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 15px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)

        # === 输入区域布局 ===
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.upload_button)

        # === 主布局 ===
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.chat_display, 8)
        layout.addLayout(input_layout, 1)
        self.setLayout(layout)

        # === 信号连接 ===
        self.send_button.clicked.connect(self.chat)
        self.input_box.returnPressed.connect(self.chat)
        self.upload_button.clicked.connect(self.upload_image)

    def chat(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return
        self.input_box.clear()

        # === 用户消息 ===
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertHtml(
            f"<div align='right'><span style='background-color: #d0f0ff; padding: 8px; border-radius: 10px;'>"
            f"<b>你：</b> {user_input}</span></div><br>"
        )

        # === 洛托姆回答 ===
        response = ask_gpt(user_input)
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertHtml(
            f"<div align='left'><span style='background-color: #fff2cc; padding: 8px; border-radius: 10px;'>"
            f"<b>ロトム：</b> {response}</span></div><br>"
        )
        self.chat_display.setTextCursor(cursor)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            # 显示你上传了图片
            cursor = self.chat_display.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertHtml(
                f"<div align='right'><span style='background-color: #e0f7fa; padding: 8px; border-radius: 10px;'>"
                f"<b>你：</b> 上传了一张图片</span></div><br>"
            )

            # 调用 vision 模块
            description = describe_image(file_path)

            # 洛托姆描述结果
            cursor = self.chat_display.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertHtml(
                f"<div align='left'><span style='background-color: #fff2cc; padding: 8px; border-radius: 10px;'>"
                f"<b>ロトム：</b> {description}</span></div><br>"
            )
            self.chat_display.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())