# main.py
import gradio as gr
import traceback
from data_loader import load_and_vectorize_documents
from llm_service import LLMService
from audio_service import AudioService
from config import WELCOME_TEXT, WELCOME_AUDIO_FILE

# 初始化服務
try:
    vector_store, retriever = load_and_vectorize_documents()
    llm_service = LLMService(retriever)
    audio_service = AudioService()
except Exception as e:
    print(f"初始化服務錯誤：{e}")
    exit()

# 全域對話歷史記錄
conversation_history = []


def intro():
    """Gradio 介面的初始介紹。"""
    # 可以在這裡添加重置對話歷史的邏輯，確保每次頁面載入時都是新的對話
    global conversation_history
    conversation_history = []  # 確保重新載入時也清空歷史
    return f"🧋 店員：{WELCOME_TEXT}", WELCOME_AUDIO_FILE


def chat_with_voice(audio_path):
    """
    處理音頻輸入、生成 LLM 回覆並回傳音頻輸出的主要函數。
    """
    global conversation_history
    try:
        # ... (這裡的 chat_with_voice 函數內容保持不變，如同我上次提供的版本) ...
        # 步驟 1：語音轉文字 (現在 Whisper 會回傳文本和偵測到的語言)
        raw_text, detected_lang_by_whisper = audio_service.transcribe_audio(audio_path)
        print(f"DEBUG (main.py): Whisper transcribed raw text: '{raw_text}'")
        print(f"DEBUG (main.py): Whisper detected language: '{detected_lang_by_whisper}'")

        # 步驟 2：使用 LLM 校正語音轉文字
        corrected_text = llm_service.correct_speech_to_text(raw_text, "")
        print(f"DEBUG (main.py): LLM corrected text (original language): '{corrected_text}'")

        # 步驟 3：將校正後的文本翻譯成中文 (用於 RAG 查詢)
        if detected_lang_by_whisper.lower() not in ["zh-tw"]:
            query_for_rag = llm_service.translate_to_chinese(corrected_text, detected_lang_by_whisper)
            print(f"DEBUG (main.py): Translated query for RAG: '{query_for_rag}'")
        else:
            query_for_rag = corrected_text
            print(f"DEBUG (main.py): Query for RAG (already zh-tw): '{query_for_rag}'")

        # 步驟 4：獲取 RAG 上下文
        rag_context = llm_service.get_rag_context(query_for_rag)

        # 步驟 5：獲取 LLM 回覆
        answer = llm_service.get_llm_response(
            corrected_text,
            conversation_history,
            rag_context,
            output_lang=detected_lang_by_whisper  # 使用 Whisper 偵測到的語言
        )
        print(f"DEBUG (main.py): LLM generated answer: '{answer}'")

        # 步驟 6：文字轉語音
        audio_output_path = audio_service.text_to_speech(answer, user_input_lang=detected_lang_by_whisper)
        print(f"DEBUG (main.py): TTS output audio path: '{audio_output_path}'")

        # 步驟 7：更新歷史記錄並顯示
        conversation_history.append((query_for_rag, answer))
        chat_log_text = ""  # 改用 chat_log_text 避免與 outputs 變數名衝突
        for q, a_log in conversation_history:
            chat_log_text += f"👤 客人：{q}\n🧋 店員：{a_log}\n\n"

        return chat_log_text.strip(), audio_output_path  # 這裡返回 chat_log_text

    except Exception as e:
        print(f"❌ 發生錯誤：{traceback.format_exc()}")
        return f"❌ 發生錯誤：{traceback.format_exc()}", None


# ========== 新增的重置函數 ==========
def reset_chat():
    """重置聊天歷史記錄和 Gradio 介面。"""
    global conversation_history
    conversation_history = []  # 清空對話歷史
    print("DEBUG (main.py): Chat history reset.")
    # 返回空字串和 None 以清空 Gradio 介面上的文本框和音頻播放器
    return "", None, f"🧋 店員：{WELCOME_TEXT}", audio_service._initialize_welcome_audio()  # 返回歡迎詞和音頻


# Gradio 介面
with gr.Blocks() as demo:
    gr.Markdown("🧋 **語音點餐系統 - 多語版本**")

    # 定義輸出口件 (Output Components)，以便重置函數可以引用它們
    chat_log_display = gr.Textbox(label="對話紀錄", lines=15)
    audio_output_display = gr.Audio(label="語音回覆", autoplay=True)

    # 設置初始歡迎訊息，並將其輸出到 chat_log_display 和 audio_output_display
    demo.load(fn=intro, inputs=[], outputs=[chat_log_display, audio_output_display])

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="請開啟麥克風")
        # 將 chat_with_voice 的輸出指向新的 chat_log_display 和 audio_output_display
        audio_input.change(fn=chat_with_voice, inputs=audio_input, outputs=[chat_log_display, audio_output_display])

    # 新增一個重置按鈕
    reset_btn = gr.Button("重置聊天")
    # 當按鈕被點擊時，呼叫 reset_chat 函數，並更新 chat_log_display 和 audio_output_display
    reset_btn.click(
        fn=reset_chat,
        inputs=[],
        outputs=[chat_log_display, audio_output_display, chat_log_display, audio_output_display]
        # 重複 chat_log_display 和 audio_output_display 確保刷新
    )

if __name__ == "__main__":
    demo.launch(debug=True, share=True)