from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl, QCoreApplication
import os

class SFX:
    def __init__(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/sfx"))
        self.click = self._load(base_path, "mixkit-message-pop-alert-2354.mp3")
        self.send = self._load(base_path, "mixkit-long-pop-2358.wav")
        self.shutter = self._load(base_path, "mixkit-camera-shutter-hard-click-1430.wav")
        self.voice_start = self._load(base_path, "mixkit-soap-bubble-sound-2925.wav")
        self.voice_end = self._load(base_path, "mixkit-soap-bubble-sound-2925.wav")

    def _load(self, base_path, name):
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(os.path.join(base_path, name)))
        effect.setVolume(0.7)
        return effect

    def play(self, sound):
        if sound.isLoaded():
            sound.play()

sfx = SFX()