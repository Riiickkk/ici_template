import os
import tempfile
import whisper
from gtts import gTTS
from gtts.lang import tts_langs
from langdetect import detect # 雖然現在優先使用 Whisper 偵測，但仍保留以防萬一

from config import LANG_MAP, WELCOME_TEXT, WELCOME_AUDIO_FILE

class AudioService:
    def __init__(self):
        # 載入 Whisper 模型
        # 警告: FP16 is not supported on CPU; using FP32 instead 是正常的，表示在 CPU 上會使用 FP32
        self.whisper_model = whisper.load_model("base")
        self.supported_tts_langs = tts_langs() # gTTS 支援的語言列表
        self._initialize_welcome_audio()

    def _initialize_welcome_audio(self):
        """如果歡迎音頻檔案不存在，則生成它。"""
        if not os.path.exists(WELCOME_AUDIO_FILE):
            tts = gTTS(text=WELCOME_TEXT, lang="zh-TW")
            tts.save(WELCOME_AUDIO_FILE)

    def transcribe_audio(self, audio_path):
        """
        使用 Whisper 將音頻轉錄為文字，並回傳偵測到的語言。
        Args:
            audio_path (str): 音頻檔案的路徑。
        Returns:
            tuple: (轉錄的文本, Whisper 偵測到的語言代碼)
        """
        whisper_result = self.whisper_model.transcribe(audio_path)
        # Whisper 的結果中通常包含 'language' 鍵
        detected_lang_by_whisper = whisper_result.get("language", "en") # 如果沒有偵測到，預設為英文
        print(f"DEBUG (AudioService): Whisper detected language: {detected_lang_by_whisper}")
        return whisper_result["text"], detected_lang_by_whisper

    def text_to_speech(self, text, user_input_lang=None):
        """
        將文字轉換為語音，優先使用提供的語言代碼 (例如來自 Whisper)，
        如果沒有提供則嘗試使用 langdetect 偵測。
        Args:
            text (str): 待轉換為語音的文本。
            user_input_lang (str, optional): 預期的語言代碼 (e.g., 'en', 'ko', 'zh-TW')。
                                             如果提供，將優先使用此語言。
        Returns:
            str: 生成的音頻檔案路徑。
        """
        if user_input_lang:
            detected_lang = user_input_lang
            print(f"DEBUG (AudioService): Using provided language for TTS: {detected_lang}")
        else:
            try:
                detected_lang = detect(text)
                print(f"DEBUG (AudioService): Detected raw language by langdetect for TTS: {detected_lang}")
            except Exception:
                detected_lang = "en" # 如果語言檢測失敗，則回退
                print(f"DEBUG (AudioService): langdetect failed for TTS, falling back to: {detected_lang}")

        # 將偵測到的語言代碼映射到 gTTS 支援的格式
        tts_lang = LANG_MAP.get(detected_lang.lower(), "en")
        print(f"DEBUG (AudioService): Mapped TTS language: {tts_lang}")
        if tts_lang not in self.supported_tts_langs:
            print(f"DEBUG (AudioService): {tts_lang} not supported by gTTS. Falling back to English.")
            tts_lang = "en"  # 回退

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts = gTTS(text=text, lang=tts_lang)
            tts.save(tmpfile.name)
            return tmpfile.name
