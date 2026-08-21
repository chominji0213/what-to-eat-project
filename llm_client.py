from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from tools.weather_tool import get_weather
from tools.restaurant_tool import get_restaurant

from rich import print as rprint

def build_agent():
    llm = init_chat_model('gemini-3.1-flash-lite', model_provider='google_genai')
    memory = InMemorySaver()
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
    rprint(result)
    final_result = result['messages'][-1].content[0]['text']
    
    return final_result

if __name__ == "__main__":
    # 터미널에서 python llm_client.py로 테스트
    agent = build_agent()
    #print(ask(agent, "강남에서 양식 맛집 추천해줘", "test-thread"))
    print(ask(agent, "오늘 서울 날씨 보고 어울리는 메뉴와 맛집 추천해줘", "test-thread"))
