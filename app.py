import streamlit as st
import uuid
from llm_client import build_agent, ask

# TODO 1: st.title("...")로 페이지 제목 표시
#   예: st.title("오늘 뭐 먹지 추천봇")

# TODO 2: 에이전트를 세션당 한 번만 생성 (지난 프로젝트와 동일 패턴)
#   if "agent" not in st.session_state:
#       st.session_state.agent = build_agent()

# TODO 3: thread_id도 세션당 한 번만 생성
#   if "thread_id" not in st.session_state:
#       st.session_state.thread_id = str(uuid.uuid4())

# TODO 4: 화면 표시용 대화 기록 리스트 준비
#   if "messages" not in st.session_state:
#       st.session_state.messages = []

# TODO 5: 지금까지 쌓인 대화 기록을 화면에 순서대로 그리기
#   for msg in st.session_state.messages:
#       with st.chat_message(msg["role"]):
#           st.write(msg["content"])

# TODO 6: 사용자 입력창
#   user_input = st.chat_input("오늘 뭐 먹을지 고민이면 물어보세요")

# TODO 7: if user_input: 블록 안에서 (지난 프로젝트와 완전히 동일한 패턴)
#   1) st.session_state.messages.append({"role": "user", "content": user_input})
#   2) with st.chat_message("user"): st.write(user_input)
#   3) answer = ask(st.session_state.agent, user_input, st.session_state.thread_id)
#   4) st.session_state.messages.append({"role": "assistant", "content": answer})
#   5) with st.chat_message("assistant"): st.write(answer)
