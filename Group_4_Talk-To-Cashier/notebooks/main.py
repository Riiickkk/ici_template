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
        # 步驟 1：語音轉文字 (現在 Whisper 會回傳文本和偵測到的語言)
        raw_text, detected_lang_by_whisper = audio_service.transcribe_audio(audio_path)
        print(f"DEBUG (main.py): Whisper transcribed raw text: '{raw_text}'")
        print(f"DEBUG (main.py): Whisper detected language: '{detected_lang_by_whisper}'")

        # 步驟 2：使用 LLM 校正語音轉文字
        # 這裡的 corrected_text 仍然是原始語言，只是修正了辨識錯誤
        corrected_text = llm_service.correct_speech_to_text(raw_text, "") # RAG context 暫時傳空字串，因為還沒翻譯
        print(f"DEBUG (main.py): LLM corrected text (original language): '{corrected_text}'")

        # 步驟 3：將校正後的文本翻譯成中文 (用於 RAG 查詢)
        # 只有當偵測到的語言不是中文時才進行翻譯
        if detected_lang_by_whisper.lower() not in ["zh", "zh-tw", "zh-cn"]:
            query_for_rag = llm_service.translate_to_chinese(corrected_text, detected_lang_by_whisper)
            print(f"DEBUG (main.py): Translated query for RAG: '{query_for_rag}'")
        else:
            query_for_rag = corrected_text # 如果是中文，則直接使用校正後的中文文本
            print(f"DEBUG (main.py): Query for RAG (already Chinese): '{query_for_rag}'")


        # 步驟 4：獲取 RAG 上下文（現在使用翻譯後的中文查詢）
        rag_context = llm_service.get_rag_context(query_for_rag)
        print(f"DEBUG (main.py): RAG context retrieved: '{rag_context}'")

        # 步驟 5：獲取 LLM 回覆 (LLM 會根據原始語言和 RAG context 回覆)
        # 這裡仍然使用 corrected_text (原始語言) 傳給 LLM，因為 LLM 知道要用顧客的語言回覆
        answer = llm_service.get_llm_response(corrected_text, conversation_history, rag_context)
        print(f"DEBUG (main.py): LLM generated answer: '{answer}'")


        # 步驟 6：文字轉語音（使用 Whisper 偵測到的語言來回覆）
        audio_output_path = audio_service.text_to_speech(answer, user_input_lang=detected_lang_by_whisper)

        # 步驟 7：更新歷史記錄並顯示
        conversation_history.append((corrected_text, answer)) # 歷史記錄仍記錄原始語言的問答

        chat_log = ""
        for q, a in conversation_history:
            chat_log += f"👤 客人：{q}\n🧋 店員：{a}\n\n"

        return chat_log.strip(), audio_output_path

    except Exception as e:
        return f"❌ 發生錯誤：{traceback.format_exc()}", None

# Gradio 介面
with gr.Blocks() as demo:
    gr.Markdown("🧋 **語音點餐系統 - 多語版本**")

    audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="請開啟麥克風")
    chat_log = gr.Textbox(label="對話紀錄", lines=15)
    audio_output = gr.Audio(label="語音回覆", autoplay=True)

    audio_input.change(fn=chat_with_voice, inputs=audio_input, outputs=[chat_log, audio_output])
    demo.load(fn=intro, inputs=[], outputs=[chat_log, audio_output])

if __name__ == "__main__":
    demo.launch(debug=True, share=True)
