import os
# from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOpenAI(
    model='gpt-3.5-turbo',
    temperature=0.3,
    api_key=os.getenv('OPENAI_API_KEY')
)

# agent = create_agent(llm)

def ask_medical_bot(question: str):
    system_msg = SystemMessage("你是一位專業的家庭醫師。")
    messages = [
        system_msg,
        HumanMessage(question),
        AIMessage('內容中若有包含簡體中文，請將簡體中文改成繁體中文。')
    ]
    response = llm.invoke(messages)
    return response.content