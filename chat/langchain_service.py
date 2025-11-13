import os
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, AIMessage

def get_llm():
    return ChatOpenAI(
        model='gpt-3.5-turbo',
        temperature=0.3,
        api_key=os.getenv('OPENAI_API_KEY'),
        streaming=True
    )

def ask_medical_bot(question: str):
    llm = get_llm()
    system_msg = SystemMessage("你是一位專業的家庭醫師。請提供正確、安全的醫學資訊。")
    messages = [
        system_msg,
        HumanMessage(question),
        AIMessage('內容中若有包含簡體中文，請將簡體中文改成繁體中文。')
    ]
    response = llm.invoke(messages)
    return response.content

def ask_medical_bot_sse(question: str):
    llm = get_llm()
    system_msg = SystemMessage("你是一位專業的家庭醫師。請提供正確、安全的醫學資訊。")
    messages = [
        system_msg,
        HumanMessage(question),
        AIMessage('內容中若有包含簡體中文，請將簡體中文改成繁體中文。')
    ]

    def generate():
        for chunk in llm.stream(messages):
            delta = getattr(chunk, "content", None)
            if delta:
                yield delta
        yield "[END]"  # 用於通知前端完成


    return generate