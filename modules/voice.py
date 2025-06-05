# modules/voice.py

import numpy as np
import sounddevice as sd
import scipy.io.wavfile
import tempfile
from faster_whisper import WhisperModel
import torch

# 初始化 Whisper 模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel("small", device=device, compute_type="float16" if device == "cuda" else "int8")

class VoiceRecorder:
    def __init__(self, samplerate=16000, max_duration=20):
        self.samplerate = samplerate
        self.max_duration = max_duration
        self.audio_buffer = []
        self.is_recording = False

    def start_recording(self):
        self.audio_buffer = []
        self.is_recording = True
        block_size = 1024

        def callback(indata, frames, time, status):
            if self.is_recording:
                self.audio_buffer.append(indata.copy())
            else:
                raise sd.CallbackStop()

        self.stream = sd.InputStream(samplerate=self.samplerate, channels=1, dtype="int16",
                                     blocksize=block_size, callback=callback)
        self.stream.start()
        sd.sleep(int(self.max_duration * 1000))  # 最长录音时间
        self.stream.stop()

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop()

    def transcribe(self) -> str:
        if not self.audio_buffer:
            return "❌ 没有录音数据。"

        audio_data = np.concatenate(self.audio_buffer, axis=0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            scipy.io.wavfile.write(tmpfile.name, self.samplerate, audio_data)
            segments, info = model.transcribe(tmpfile.name, beam_size=5, language=None)
            text_output = "".join(s.text.strip() for s in segments)
            return f"{text_output}" if text_output else "❌ 无法识别语音。"

