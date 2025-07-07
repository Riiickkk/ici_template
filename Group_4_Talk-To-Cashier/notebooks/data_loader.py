import os
import glob
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config import DATA_FOLDER_PATH

def load_and_vectorize_documents():
    """
    從指定資料夾載入文件，分割它們，並建立 Chroma 向量儲存。
    回傳向量儲存和檢索器。
    """
    all_files = glob.glob(DATA_FOLDER_PATH) # 從 config.py 獲取 DATA_FOLDER_PATH
    docs_all = []

    for file_path in all_files:
        ext = os.path.splitext(file_path)[-1].lower()
        try:
            if ext == ".csv":
                loader = CSVLoader(file_path=file_path, encoding='big5')
                docs = loader.load()
                docs_all.extend(docs)
                print(f"✅ 載入 CSV：{file_path}")
            elif ext == ".pdf":
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                docs_all.extend(docs)
                print(f"✅ 載入 PDF：{file_path}")
            else:
                print(f"⚠️ 不支援的檔案類型：{file_path}")
        except Exception as e:
            print(f"❌ 載入失敗：{file_path}，錯誤：{e}")

    if not docs_all:
        raise ValueError("沒有載入任何文件。請檢查資料夾和檔案路徑。")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs_all)
    vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    print('完成向量化')

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    return vector_store, retriever

def format_docs(docs):
    """將檢索到的文件格式化為單一字串。"""
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    # 範例用法（用於測試）
    vector_store, retriever = load_and_vectorize_documents()
    # 您現在可以使用檢索器來獲取相關文件
    # retrieved_docs = retriever.get_relevant_documents("我想點一杯紅茶")
    # print(format_docs(retrieved_docs))