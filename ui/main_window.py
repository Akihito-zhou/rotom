import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextBrowser, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# 让你可以导入 modules.chat
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules.chat import ask_gpt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("洛托姆助手")
        self.setFixedSize(480, 720)  # 模拟手机洛托姆形状

        # === 设置背景图（使用 QLabel，不被遮挡）===
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assets/rotom_bg (1).png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()  # 放到最底层

        # === 聊天窗口 ===
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

        # === 底部输入区域 ===
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # === 主布局 ===
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.chat_display, 8)
        layout.addLayout(input_layout, 1)
        self.setLayout(layout)

        # === 信号连接 ===
        self.send_button.clicked.connect(self.chat)
        self.input_box.returnPressed.connect(self.chat)

    def chat(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return
        self.input_box.clear()

        # === 使用 QTextCursor 手动控制对齐 ===
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        user_html = (
            f"<div align='right'>"
            f"<span style='background-color: #d0f0ff; padding: 8px; border-radius: 10px;'>"
            f"<b>你：</b> {user_input}</span></div><br>"
        )
        cursor.insertHtml(user_html)
        self.chat_display.setTextCursor(cursor)

        # === 获取洛托姆回复 ===
        response = ask_gpt(user_input)

        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        rotom_html = (
            f"<div align='left'>"
            f"<span style='background-color: #fff2cc; padding: 8px; border-radius: 10px;'>"
            f"<b>ロトム：</b> {response}</span></div><br>"
        )
        cursor.insertHtml(rotom_html)
        self.chat_display.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())