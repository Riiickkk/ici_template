import os
import tempfile
import whisper
from gtts import gTTS
from gtts.lang import tts_langs
from langdetect import detect
from config import LANG_MAP, WELCOME_TEXT, WELCOME_AUDIO_FILE

class AudioService:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.supported_tts_langs = tts_langs()
        self._initialize_welcome_audio()

    def _initialize_welcome_audio(self):
        """如果歡迎音頻檔案不存在，則生成它。"""
        if not os.path.exists(WELCOME_AUDIO_FILE):
            tts = gTTS(text=WELCOME_TEXT, lang="zh-TW")
            tts.save(WELCOME_AUDIO_FILE)

    def transcribe_audio(self, audio_path):
        """使用 Whisper 將音頻轉錄為文字。"""
        whisper_result = self.whisper_model.transcribe(audio_path)
        return whisper_result["text"]

    def text_to_speech(self, text, user_input_lang=None):
        """將文字轉換為語音，檢測語言或使用提供的語言。"""
        if user_input_lang:
            detected_lang = user_input_lang
        else:
            try:
                detected_lang = detect(text)
            except Exception:
                detected_lang = "en" # 如果語言檢測失敗，則回退

        tts_lang = LANG_MAP.get(detected_lang.lower(), "en")
        if tts_lang not in self.supported_tts_langs:
            tts_lang = "en"  # 回退

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts = gTTS(text=text, lang=tts_lang)
            tts.save(tmpfile.name)
            return tmpfile.name