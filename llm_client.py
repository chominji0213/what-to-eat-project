import sqlite3
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from tools.weather_tool import get_weather
from tools.restaurant_tool import get_restaurant

from rich import print as rprint

def build_agent():
    llm = init_chat_model('gemini-3.1-flash-lite', model_provider='google_genai')

    conn = sqlite3.connect('checkpoint.db', check_same_thread=False)
    memory = SqliteSaver(conn)
    
    eat_agent = create_agent(
        model=llm,
        tools=[get_weather, get_restaurant],
        checkpointer=memory,
        system_prompt="너는 기분/날씨/시간대에 맞는 메뉴와 맛집을 추천하는 챗봇이야. 필요하면 날씨를 먼저 확인하고, 그 결과를 참고해서 맛집을 추천해줘. 맛집을 추천할 땐 지역명이나 음식 종류를 파악해서 검색해줘. 다만 만약 사용자가 날씨에 대해서 물었거나 굳이 먼저 메뉴를 물어보지 않으면 사용자의 질문에 맞는것만 대답해"
    )

    return eat_agent


def ask(agent, user_message: str, thread_id: str) -> str:
    config = {'configurable': {'thread_id': thread_id}}
    result = agent.invoke({'messages': [HumanMessage(content=user_message)]}, config)
    final_result = result['messages'][-1].content[0]['text']
    
    return final_result

# ============================================================
# 시즌2 (대화 기억 + 실시간 응답) 에서 새로 추가할 부분
# ============================================================
def ask_stream(agent, user_message: str, thread_id: str):
    """
    ask()와 동일한 역할이지만, 답변을 한 번에 반환하지 않고
    토큰(글자) 단위로 실시간으로 흘려보내는(streaming) 버전.
    """
    config = {'configurable': {'thread_id': thread_id}}
    result = agent.stream({'messages': [HumanMessage(content=user_message)]}, config, stream_mode='messages')
    for message_chunk, metadata in result:
        content = message_chunk.content

        if not isinstance(content, list):   #content가 리스트가 아니라면
            continue

        #타이핑 하듯이 보이게
        for part in content:
            if isinstance(part, dict) and part.get('type') == 'text':
                text = part.get('text', '')
                if text:
                    yield text


if __name__ == "__main__":
    agent = build_agent()
    for piece in ask_stream(agent, "강남 맛집 추천해줘", "stream-test-2"):
        print(piece, end="", flush=True)
