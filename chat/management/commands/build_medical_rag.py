import os
from django.core.management.base import BaseCommand
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Step 1: 讀取醫療資料...')

        # 取得目前這支指令所在的 chat/management/commands/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # chat/medical_docs 資料夾
        medical_docs_path = os.path.join(current_dir, "../../medical_docs")
        medical_docs_path = os.path.abspath(medical_docs_path)

        # 1. 載入醫療文件(load)
        loader =DirectoryLoader(medical_docs_path, glob="**/*.txt", loader_cls=TextLoader)
        docs = loader.load()
        print(f'載入{len(docs)}筆文件')

        if len(docs) == 0:
            print('❌ 沒有任何文件')
            return
        
        # 2. 切割文本(chunk)
        print('Step 2: 切割文本...')
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
        )
        split_docs = splitter.split_documents(docs)

        # 3. 向量化(embedding)
        print('Step 3: 產生向量 Embeddings...')
        embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))

        # 4. 儲存至向量資料庫(store)
        print('Step 4: 儲存到 Chroma 資料庫...')
        Chroma.from_documents(split_docs, embeddings, persist_directory='chroma_db')
        print('醫療 RAG 向量資料庫建立完成！')

