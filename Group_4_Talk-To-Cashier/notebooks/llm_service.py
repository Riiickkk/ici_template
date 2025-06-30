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
        self.client = OpenAI(api_key=OPENAI_API_KEY) # 用於校正提示

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

    def get_llm_response(self, corrected_text, conversation_history, rag_context):
        """根據校正後的文字和對話歷史獲取 LLM 的回覆。"""
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(rag_context=rag_context)
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