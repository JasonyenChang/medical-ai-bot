import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.messages import SystemMessage, HumanMessage, AIMessage

embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))

def rag_retrieve(query: str, k = 3):
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    retriever = db.as_retriever()
    results = retriever._get_relevant_documents(query, run_manager=None)
    return results

def rag_generate_stream(query: str):
    # 1. 取出文本片段
    docs = rag_retrieve(query)
    context = '\n\n'.join([doc.page_content for doc in docs])

    has_data = len(context.strip()) > 0

    # 若沒有檢索結果 → 直接回覆固定句子
    if not has_data:
        def generate_no_data():
            yield "很抱歉，這問題不在我的專業範圍內。"
            yield "[END]"
        return generate_no_data

    # 2. 建立 LLM（串流模式）
    llm = ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.3,
        api_key=os.getenv('OPENAI_API_KEY'),
        streaming=True
    )

    # 3. 建立 prompt
    question = (
        "你是一位專業的家庭醫師，你的所有回答都【必須】僅根據以下提供的醫療資料。\n"
        "如果資料中找不到答案，請回覆：『很抱歉，這問題不在我的專業範圍內。』\n"
        "你不可自行推論內容，不可編造答案，不可使用醫療資料外的資訊。\n"
        "回答內容請使用繁體中文，並保持專業、謹慎且具醫療安全性。\n\n"
        f"=== 醫療資料 ===\n{context}\n\n"
        f"=== 使用者問題 ===\n{query}\n"
        "請開始回答："
    )

    system_msg = SystemMessage(question)
    messages = [
        system_msg,
        AIMessage('內容中若有包含簡體中文，請將簡體中文改成繁體中文。')
    ]

    # 4. Streaming 逐段產生
    def generate():
        for chunk in llm.stream(messages):
            delta = chunk.content
            if delta:
                yield delta
        yield "[END]"

    return generate
