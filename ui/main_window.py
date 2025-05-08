import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit
from modules.chat import ask_gpt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("洛托姆助手")
        self.resize(400, 500)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_box = QLineEdit()
        self.send_button = QPushButton("发送")

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        self.send_button.clicked.connect(self.chat)

    def chat(self):
        user_input = self.input_box.text()
        if not user_input:
            return
        self.chat_display.append(f"你：{user_input}")
        response = ask_gpt(user_input)
        self.chat_display.append(f"洛托姆：{response}\n")
        self.input_box.clear()