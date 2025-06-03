import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextBrowser, QLineEdit, QPushButton, QLabel, QFileDialog
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from urllib.parse import quote

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 模块导入
from modules.chat import ask_gpt
from modules.vision import describe_image

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("洛托姆助手 | Rotom VQA")
        self.setFixedSize(480, 720)
        self.setWindowIcon(QIcon("assets/rotom_icon.png"))

        bg_path = os.path.join(os.path.dirname(__file__), "assets", "rotom_frame.png")
        bg_path = os.path.abspath(bg_path).replace("\\", "/")  # Windows 下路径格式处理

        # 背景图
        self.bg_label = QLabel(self)
        pixmap = QPixmap(bg_path)
        self.bg_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.raise_()  # 把背景图放到最底层

        # 聊天框
        self.chat_display = QTextBrowser(self)
        self.chat_display.setMaximumHeight(720)
        self.chat_display.setMaximumWidth(480)
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: rgba(255, 255, 255, 0);
                border-radius: 20px;
                padding: 14px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
        """)

        # 输入框
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("ロトムに話しかけてみよう")
        self.input_box.setFixedHeight(28)
        self.input_box.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border-radius: 10px;
                font-size: 14px;
                height: 24px;
            }
        """)

        # 发送按钮
        self.send_button = QPushButton("发送", self)
        self.send_button.setFixedHeight(28)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4D4D;
                color: white;
                border-radius: 14px;
                padding: 4px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF7373;
            }
        """)

        # 上传按钮
        self.upload_button = QPushButton("📷", self)
        self.upload_button.setFixedHeight(28)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)

        # 聊天框：靠上，尺寸合适
        self.chat_display.setGeometry(60, 165, 360, 505)

        # 输入框 + 按钮：靠下排一行（左到右）
        self.input_box.setGeometry(40, 680, 260, 32)        # 输入框在左
        self.send_button.setGeometry(310, 680, 60, 32)       # 发送按钮在中
        self.upload_button.setGeometry(380, 680, 32, 32)     # 上传按钮在右

        # 信号连接
        self.send_button.clicked.connect(self.chat)
        self.input_box.returnPressed.connect(self.chat)
        self.upload_button.clicked.connect(self.upload_image)

    def append_message(self, sender: str, text: str, side: str, is_html=False):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)

        align = "left" if side == "left" else "right"
        bubble_color = "#f0f8ff" if side == "left" else "#c7c5b3"

        html = (
            f"<table width='100%'><tr><td align='{align}'>"
            f"<div style='padding:10px; border-radius:12px; font-size:14px; "
            f"font-family:'Segoe UI'; display:inline-block; max-width:80%; "
            f"background-color:{bubble_color}; margin:6px 0;'>"
        )

        if is_html:
            html += f"<b style='color:gray'>{sender}：</b><br>{text}</div></td></tr></table><br>"
        else:
            html += f"<b style='color:gray'>{sender}：</b> {text}</div></td></tr></table><br>"

        cursor.insertHtml(html)
        self.chat_display.setTextCursor(cursor)

    def chat(self):
        user_input = self.input_box.text().strip()
        if not user_input:
            return
        self.input_box.clear()

        self.append_message("你", user_input, "right")
        response_html = ask_gpt(user_input)
        self.append_message("ロトム", response_html, "left", is_html=True)

        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"
            img_html = (
                f"<div style='max-width:280px; margin-top:10px;'>"
                f"<img src='{file_url}' style='width:100%; height:auto; border-radius:12px; box-shadow:0 0 8px #ccc;'>"
                f"</div>"
            )
            self.append_message("你", f"上传了一张图片<br>{img_html}", "right", is_html=True)

            description = describe_image(file_path).replace("\n", "<br>")
            self.append_message("ロトム", description, "left", is_html=True)

