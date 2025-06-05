import sys
import os
import threading
import cv2
import time
from PyQt5.QtWidgets import (
    QWidget, QTextBrowser, QLineEdit, QPushButton, QLabel, QFileDialog, QMenu, QDialog
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QEvent
from urllib.parse import quote
from modules.multi_language.language_handler import generate_multilingual_response
from modules.pokemon_images_detection.find_match import find_best_match
from modules.chat import query_local
from modules.llm.chatgpt_rotom import ask_chatgpt_with_image
from modules.intent import extract_entity_name, extract_fields
from modules.voice import VoiceRecorder
from modules.vision import CameraCaptureDialog

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
        self.setAcceptDrops(True)  # 启用拖拽功能
        self.pending_image = None  # 用于存储待处理的图片路径
        self.voice_recorder = VoiceRecorder()
        self.recording_thread = None


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
                font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif;
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
                font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif;
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
                font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif;
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
                font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif;                        
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)

        # 创建菜单
        upload_menu = QMenu(self)
        upload_menu.addAction("📁 上传图片", self.upload_image)
        upload_menu.addAction("📸 拍照识别", self.capture_from_camera)

        self.upload_button.setMenu(upload_menu)

        # 语音按钮
        self.voice_button = QPushButton("🎤", self)
        self.voice_button.setFixedHeight(28)
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif;                        
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
        """)
        # 启用事件监听
        self.voice_button.setMouseTracking(True)
        self.voice_button.installEventFilter(self)

        # 聊天框：靠上，尺寸合适
        self.chat_display.setGeometry(60, 165, 360, 505)

        # 输入框 + 按钮：靠下排一行（左到右）
        self.input_box.setGeometry(40, 680, 260, 32)        # 输入框在左
        self.send_button.setGeometry(310, 680, 60, 32)       # 发送按钮在中
        self.upload_button.setGeometry(380, 680, 32, 32)     # 上传按钮在右
        self.voice_button.setGeometry(420, 680, 32, 32)

        # 信号连接
        self.send_button.clicked.connect(self.chat)
        self.input_box.returnPressed.connect(self.chat)
        self.upload_button.clicked.connect(self.upload_image)
        self.voice_button.installEventFilter(self)

    def append_message(self, sender: str, text: str, side: str, is_html=False):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)

        align = "left" if side == "left" else "right"
        bubble_color = "#f0f8ff" if side == "left" else "#c7c5b3"

        html = (
            f"<table width='100%'><tr><td align='{align}'>"
            f"<div style='padding:10px; border-radius:12px; font-size:14px; "
            f"font-family: 'Noto Sans', 'Noto Sans SC', 'Noto Sans JP', sans-serif; display:inline-block; max-width:80%; "
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
        self.input_box.clear()

        if self.pending_image:
            # 有图片待处理
            file_path = self.pending_image
            self.pending_image = None  # 清空暂存路径
            self.process_image_and_question(file_path, user_input)
        else:
            # 无图片，纯文字输入
            self.append_message("你", user_input, "right")
            response_html = ask_gpt(user_input)
            self.append_message("ロトム", response_html, "left", is_html=True)

        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )


        # 添加拖拽事件
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.pending_image = file_path  # 暂存图片路径
                file_url = f"file:///{quote(file_path.replace(os.sep, '/'))}"
                img_html = f"<div style='max-width:280px;'><img src='{file_url}' style='width:100%; border-radius:12px; box-shadow:0 0 8px #ccc;'></div>"
                self.append_message("你", f"上传了一张图片<br>{img_html}", "right", is_html=True)

        #上传图片
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
    
        # 拍照识别
    def capture_from_camera(self):
        dialog = CameraCaptureDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.captured_path:
            image_path = dialog.captured_path

            from urllib.parse import quote
            from os.path import abspath
            file_url = f"file:///{quote(abspath(image_path).replace(os.sep, '/'))}"

            img_html = (
                f"<div style='max-width:280px; margin-top:10px;'>"
                f"<img src='{file_url}' style='width:100%; height:auto; border-radius:12px; box-shadow:0 0 8px #ccc;'>"
                f"</div>"
            )
            self.append_message("你", f"拍摄了一张图片<br>{img_html}", "right", is_html=True)

            from modules.vision import describe_image
            result_html = describe_image(image_path).replace("\n", "<br>")
            self.append_message("ロトム", result_html, "left", is_html=True)


    def process_image_and_question(self, file_path, user_question):
        if user_question == "":
            # 无问题，默认查询基础信息
            description = describe_image(file_path)
            self.append_message("ロトム", description, "left", is_html=True)
        else:
            # 有问题，根据问题查询对应字段或fallback到chatgpt
            response_html = self.get_response_based_on_image(file_path, user_question)
            self.append_message("你", user_question, "right")
            self.append_message("ロトム", response_html, "left", is_html=True)


    def get_response_based_on_image(self, file_path, user_question):

        # Step 1: 使用 CLIP 做图像识别
        matches = find_best_match(file_path)
        if not matches:
            print("[DEBUG] 图像识别失败：没有找到匹配的宝可梦")
            answer = ask_chatgpt_with_image(user_question, [file_path])
            translated = generate_multilingual_response(answer, user_question)
            return f"🌐 来自ChatGPT：<br>{translated}"

        matched_path, score = matches[0]
        matched_name = os.path.basename(os.path.dirname(matched_path))

        # Step 2: 提取用户意图
        keyword = extract_entity_name(user_question)
        fields = extract_fields(user_question)

        # Debug 输出
        print(f"[DEBUG] 用户问题：「{user_question}」")
        print(f"[DEBUG] 图像识别结果：{matched_name}，相似度：{score:.2f}")
        print(f"[DEBUG] 提取的实体名：{keyword if keyword else '(未识别)'}")
        print(f"[DEBUG] 提取的字段意图：{fields if fields else '(无字段)'}")

        # Step 3: 若用户未提及关键词，默认使用图像识别的名称
        used_fallback = False
        if not keyword:
            keyword = matched_name
            used_fallback = True

        if used_fallback:
            print(f"[DEBUG] 实体名由图像识别补全为：{keyword}")

        # Step 4: 本地图鉴查询
        found, html = query_local(keyword, "pokemon", fields=fields)
        if found:
            return f"✅ 找到本地宝可梦：<b>{keyword}</b><br>{html}"
        else:
            print(f"[DEBUG] 本地图鉴未找到「{keyword}」的相关信息，fallback 到 ChatGPT")
            answer = ask_chatgpt_with_image(user_question, [file_path])
            translated = generate_multilingual_response(answer, user_question)
            return f"{translated}"

    def eventFilter(self, source, event):
        if source == self.voice_button:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.start_voice_recording()
                return True
            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                self.stop_voice_recording()
                return True
        return super().eventFilter(source, event)

    def start_voice_recording(self):
        self.append_message("系统", "🎙️ 按住录音中，请开始说话...", "left")
        self.voice_recorder = VoiceRecorder()
        self.recording_thread = threading.Thread(target=self.voice_recorder.start_recording)
        self.recording_thread.start()

    def stop_voice_recording(self):
        self.voice_recorder.stop_recording()
        self.recording_thread.join()

        result = self.voice_recorder.transcribe()
        if result.startswith("❌"):
            self.append_message("系统", result, "left")
        else:
            self.input_box.setText(result)
            self.chat()



