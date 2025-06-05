import os

project_dir = "/mnt/data/voice_ui_demo"
os.makedirs(project_dir, exist_ok=True)

# main.py
main_py = '''\
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
'''

# main_window.py
main_window_py = '''\
import random
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTextBrowser
from PyQt5.QtCore import QTimer
from voice_input import VoiceRecorder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("语音识别测试")
        self.setFixedSize(400, 300)

        self.recorder = VoiceRecorder()
        self.wave_timer = QTimer()
        self.wave_timer.timeout.connect(self.animate_wave_level)
        self.wave_level = 1

        self.voice_button = QPushButton("🎙️ 按住说话", self)
        self.voice_button.setGeometry(30, 200, 100, 40)
        self.voice_button.pressed.connect(self.start_voice_recording)
        self.voice_button.released.connect(self.stop_voice_recording)

        self.wave_label = QLabel("🎧 等待录音", self)
        self.wave_label.setGeometry(150, 200, 200, 40)

        self.input_box = QLineEdit(self)
        self.input_box.setGeometry(30, 250, 300, 30)

        self.chat_display = QTextBrowser(self)
        self.chat_display.setGeometry(30, 20, 340, 160)

    def start_voice_recording(self):
        self.wave_label.setText("🎙️ 正在录音...")
        self.wave_level = 1
        self.recorder.start()
        self.wave_timer.start(200)

    def stop_voice_recording(self):
        self.wave_timer.stop()
        self.wave_label.setText("🧠 识别中...")
        text = self.recorder.stop_and_transcribe()
        self.input_box.setText(text)
        self.chat_display.append(f"🗣️ {text}")
        self.wave_label.setText("✅ 识别完成")

    def animate_wave_level(self):
        self.wave_level = random.randint(1, 8)
        self.wave_label.setText("🎧 " + "▇" * self.wave_level)
'''

# voice_input.py
voice_input_py = '''\
import numpy as np
import sounddevice as sd
import scipy.io.wavfile
import tempfile
from faster_whisper import WhisperModel
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel("small", device=device)

class VoiceRecorder:
    def __init__(self, samplerate=16000):
        self.recording = False
        self.data = []
        self.stream = None
        self.samplerate = samplerate

    def _callback(self, indata, frames, time, status):
        if self.recording:
            self.data.append(indata.copy())

    def start(self):
        self.data = []
        self.recording = True
        self.stream = sd.InputStream(callback=self._callback, channels=1, samplerate=self.samplerate)
        self.stream.start()

    def stop_and_transcribe(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

        if not self.data:
            return "❌ 没有录到声音"

        audio = np.concatenate(self.data, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            scipy.io.wavfile.write(tmpfile.name, self.samplerate, audio)
            segments, info = model.transcribe(tmpfile.name, language=None)
            text = "".join([s.text.strip() for s in segments])
            return text or "❌ 无法识别语音"
'''

with open(f"{project_dir}/main.py", "w") as f:
    f.write(main_py)

with open(f"{project_dir}/main_window.py", "w") as f:
    f.write(main_window_py)

with open(f"{project_dir}/voice_input.py", "w") as f:
    f.write(voice_input_py)

project_dir
