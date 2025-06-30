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
    # 如果基本服務載入失敗，則退出或優雅處理
    exit()

# 全域對話歷史記錄
conversation_history = []

def intro():
    """Gradio 介面的初始介紹。"""
    return f"🧋 店員：{WELCOME_TEXT}", WELCOME_AUDIO_FILE

def chat_with_voice(audio_path):
    """
    處理音頻輸入、生成 LLM 回覆並回傳音頻輸出的主要函數。
    """
    global conversation_history
    try:
        # 步驟 1：語音轉文字
        raw_text = audio_service.transcribe_audio(audio_path)

        # 步驟 2：獲取 RAG 上下文（使用原始文字進行初始檢索）
        rag_context = llm_service.get_rag_context(raw_text)

        # 步驟 3：使用 LLM 校正語音轉文字
        corrected_text = llm_service.correct_speech_to_text(raw_text, rag_context)

        # 步驟 4：獲取 LLM 回覆
        answer = llm_service.get_llm_response(corrected_text, conversation_history, rag_context)

        # 步驟 5：文字轉語音（從校正後的文字檢測語言）
        audio_output_path = audio_service.text_to_speech(answer, user_input_lang=None) # 將從 `answer` 中檢測

        # 步驟 6：更新歷史記錄並顯示
        conversation_history.append((corrected_text, answer))

        chat_log = ""
        for q, a in conversation_history:
            chat_log += f"👤 客人：{q}\n🧋 店員：{a}\n\n"

        return chat_log.strip(), audio_output_path

    except Exception as e:
        return f"❌ 發生錯誤：{traceback.format_exc()}", None

# Gradio 介面
with gr.Blocks() as demo:
    gr.Markdown("🧋 **語音點餐系統 - 多語版本**")

    audio_input = gr.Audio(sources="upload", type="filepath", label="請上傳語音")
    chat_log = gr.Textbox(label="對話紀錄", lines=15)
    audio_output = gr.Audio(label="語音回覆", autoplay=True)

    audio_input.change(fn=chat_with_voice, inputs=audio_input, outputs=[chat_log, audio_output])
    demo.load(fn=intro, inputs=[], outputs=[chat_log, audio_output])

if __name__ == "__main__":
    demo.launch()