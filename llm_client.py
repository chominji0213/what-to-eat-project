from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from tools.weather_tool import get_weather
from tools.restaurant_tool import get_restaurant


def build_agent():
    """
    TODO 1: init_chat_model("gemini-3.1-flash-lite", model_provider="google_genai")로 llm 생성
            (지난 프로젝트와 동일)

    TODO 2: InMemorySaver() 인스턴스 하나 만들기 (memory 변수에 저장)

    TODO 3: create_agent(...)로 agent 생성
      - model=llm
      - tools=[get_weather, get_restaurant]   <- 이번엔 도구가 2개!
      - system_prompt: 이번 챗봇의 역할을 새로 적어야 함
        (예: "너는 기분/날씨/시간대에 맞는 메뉴와 맛집을 추천하는 챗봇이야.
              필요하면 날씨를 먼저 확인하고, 그 결과를 참고해서 맛집을 추천해줘.
              맛집을 추천할 땐 지역명이나 음식 종류를 파악해서 검색해줘.")
      - checkpointer=memory

    TODO 4: 완성된 agent 반환
    """
    pass


def ask(agent, user_message: str, thread_id: str) -> str:
    """
    TODO 1: config = {"configurable": {"thread_id": thread_id}} 만들기 (지난 프로젝트와 동일)

    TODO 2: agent.invoke({"messages": [HumanMessage(content=user_message)]}, config) 호출

    TODO 3: result['messages'][-1].content에서 최종 답변 꺼내기
      - 지난 프로젝트에서 content가 리스트([{"type": "text", "text": ...}]) 형태였던 것 기억하기
      - 안전하게 처리하고 싶으면 isinstance(content, list) 체크 추가 가능
    """
    pass


if __name__ == "__main__":
    # 터미널에서 python llm_client.py로 단독 테스트
    # TODO: 도구 조합 판단을 확인할 수 있는 질문들로 테스트해보기
    #   1) "강남에서 한식 맛집 추천해줘" -> get_restaurant만 호출되는지
    #   2) "오늘 서울 날씨 어때?" -> get_weather만 호출되는지
    #   3) "오늘 날씨 보고 어울리는 메뉴 추천해줘" -> 두 도구가 순서대로 호출되는지
    agent = build_agent()
    print(ask(agent, "강남에서 한식 맛집 추천해줘", "test-thread"))
