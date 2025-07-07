from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT_TEMPLATE
from data_loader import format_docs

class LLMService:
    def __init__(self, retriever):
        self.retriever = retriever
        self.model = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
        self.output_parser = StrOutputParser()
        self.client = OpenAI(api_key=OPENAI_API_KEY) # 用於校正提示和翻譯

    def translate_to_chinese(self, text: str, source_lang: str) -> str:
        """
        將輸入文本翻譯成繁體中文。
        Args:
            text (str): 待翻譯的文本。
            source_lang (str): 原始語言代碼 (e.g., 'en', 'ko', 'zh')。
        Returns:
            str: 翻譯後的繁體中文文本。
        """
        # 翻譯提示，明確指示翻譯成繁體中文
        translation_prompt = f"""請將以下文本翻譯成繁體中文。
        原始語言：{source_lang}
        文本："{text}"

        請只輸出翻譯後的繁體中文文本，不要有任何額外的解釋或贅述，同時確保語意在不同語言中仍是一致的。
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "你是一個專業的翻譯助手，專門將各種語言翻譯成繁體中文。"},
                    {"role": "user", "content": translation_prompt}
                ],
                temperature=0.1, # 翻譯任務通常使用較低的溫度
                max_tokens=200
            )
            translated_text = response.choices[0].message.content.strip()
            print(f"DEBUG (LLMService): Translated '{text}' from {source_lang} to zh-TW: '{translated_text}'")
            return translated_text
        except Exception as e:
            print(f"⚠️ 翻譯錯誤：{e}")
            # 如果翻譯失敗，回傳原始文本，讓後續流程至少能繼續
            return text

    def get_rag_context(self, query):
        """根據查詢檢索相關文件。"""
        try:
            retrieved_docs = self.retriever.get_relevant_documents(query)
            return format_docs(retrieved_docs)
        except Exception as e:
            print(f"⚠️ RAG 檢索錯誤：{e}")
            return "找不到相關資料。"

    def correct_speech_to_text(self, raw_text, rag_context):
        """校正語音轉文字的潛在錯誤。"""
        correction_prompt = f"""以下是一段可能有誤的語音轉文字內容，請幫我修正為語意通順的句子，並使用輸入語音的語言輸出文字內容，
        例如語音的語言是英文，就輸出英文，語音的語言俄文就輸出俄文，只要輸出語音內容即可，不要有任何贅述：
        【資料】：{rag_context}

        【語音轉文字內容】：「{raw_text}」

        請輸出修正後的版本，若無需修正請原樣輸出。"""
        correction_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位語音辨識助手，負責根據菜單資料幫忙校正語音辨識錯誤，不要亂改正確的詞句。"},
                {"role": "user", "content": correction_prompt}
            ],
            temperature=0.2,
            max_tokens=100
        )
        return correction_response.choices[0].message.content.strip()

    # 修改 get_llm_response 函數簽名和 system_prompt 格式化
    def get_llm_response(self, corrected_text, conversation_history, rag_context, output_lang): # <-- 新增 output_lang 參數
        """根據校正後的文字和對話歷史獲取 LLM 的回覆。"""
        # 根據 output_lang 準備更明確的語言指令
        lang_instruction_map = {
            "en": "英文", "zh-tw": "繁體中文", "zh": "繁體中文", "zh-cn": "繁體中文",
            "ja": "日文", "ko": "韓文", "es": "西班牙文", "fr": "法文",
            "de": "德文", "it": "義大利文", "pt": "葡萄牙文", "ru": "俄文",
            "hi": "印地語", "id": "印尼文", "th": "泰文", "vi": "越南文",
            "tr": "土耳其文", "pl": "波蘭文", "nl": "荷蘭文", "sv": "瑞典文",
            "ar": "阿拉伯文"
        }
        # 如果 output_lang 不在映射中，則默認顯示其代碼
        display_lang = lang_instruction_map.get(output_lang.lower(), output_lang)

        # 格式化系統提示，現在包含 output_lang_instruction
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(rag_context=rag_context, output_lang_instruction=display_lang) # <-- 新增 output_lang_instruction
        messages = [{"role": "system", "content": system_prompt}]

        for q, a in conversation_history[-100:]: # 限制歷史記錄
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})
        messages.append({"role": "user", "content": corrected_text})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()