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
    final_result = result['messages'][-1].content[0]['text']
    
    return final_result

# ============================================================
# 시즌2 (대화 기억 + 실시간 응답) 에서 새로 추가할 부분
# ============================================================

# TODO (시즌2-1): 서버가 재시작돼도 대화 기록이 유지되도록
# InMemorySaver 대신 SqliteSaver(파일 기반 체크포인터)로 바꿔보기.
#
#   from langgraph.checkpoint.sqlite import SqliteSaver
#   import sqlite3
#
#   def build_agent():
#       conn = sqlite3.connect("checkpoint.db", check_same_thread=False)
#       memory = SqliteSaver(conn)
#       ...  # 나머지는 기존 build_agent()와 동일, checkpointer=memory만 그대로 사용
#
# - requirements.txt에 langgraph-checkpoint-sqlite 이미 추가해둠
# - check_same_thread=False가 필요한 이유: Streamlit은 요청마다 다른 스레드에서 실행될 수 있어서
# - checkpoint.db 파일은 실행하면 프로젝트 폴더에 자동 생성됨 (.gitignore에 이미 추가해둠)


def ask_stream(agent, user_message: str, thread_id: str):
    """
    ask()와 동일한 역할이지만, 답변을 한 번에 반환하지 않고
    토큰(글자) 단위로 실시간으로 흘려보내는(streaming) 버전.

    TODO 1: config 구성 (ask()와 동일)
      config = {"configurable": {"thread_id": thread_id}}

    TODO 2: agent.invoke() 대신 agent.stream()으로 순회하기
      for chunk in agent.stream(
          {"messages": [HumanMessage(content=user_message)]},
          config,
          stream_mode="messages",
      ):
          ...

      - stream_mode="messages"는 LLM이 생성하는 답변 조각(토큰)을 실시간으로 넘겨줌
      - chunk가 정확히 어떤 모양인지 처음엔 rprint(chunk)로 한 번 찍어서 구조 확인해보기
        (버전에 따라 (message_chunk, metadata) 튜플일 수도 있음)

    TODO 3: chunk에서 순수 텍스트 부분만 꺼내서 yield
      - 도구 호출(tool call) 관련 메타데이터/빈 조각은 건너뛰고,
        실제 답변 글자만 yield하도록 필터링
      - 이 함수를 제너레이터로 만들면(pass 대신 yield 사용) app.py의
        st.write_stream()에 그대로 넘길 수 있음
    """
    pass


if __name__ == "__main__":
    # 터미널에서 python llm_client.py로 테스트
    agent = build_agent()
    #print(ask(agent, "강남에서 양식 맛집 추천해줘", "test-thread"))
    print(ask(agent, "오늘 서울 날씨 보고 어울리는 메뉴와 맛집 추천해줘", "test-thread"))

    # TODO: ask_stream 구현 후 아래로 테스트
    #   for piece in ask_stream(agent, "강남에서 한식 맛집 추천해줘", "test-thread-2"):
    #       print(piece, end="", flush=True)
