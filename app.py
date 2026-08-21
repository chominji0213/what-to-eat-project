import streamlit as st
import uuid
from llm_client import build_agent, ask

# TODO (시즌2-3): 여러 개의 대화(멀티 세션)를 관리하고 싶다면 여기서 사이드바 UI 구성
#   with st.sidebar:
#       if st.button("새 대화 시작"):
#           st.session_state.thread_id = str(uuid.uuid4())
#           st.session_state.messages = []
#           st.rerun()
#   -> 지금은 새로고침하면 항상 새 thread_id가 생기는데,
#      "새 대화 시작" 버튼이 생기면 명시적으로 대화를 끊고 새로 시작할 수 있음
#   (여러 개의 지난 대화 목록까지 보여주고 싶다면 st.session_state.threads = {} 형태로
#    thread_id별 messages를 따로 저장해두고 selectbox로 골라 전환하는 것도 가능 - 심화 과제)

st.title("오늘 뭐 먹지 추천봇")

if 'agent' not in st.session_state:
    st.session_state.agent = build_agent()

if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

user_input = st.chat_input('오늘 뭐 먹을지 고민이면 물어보세요.')

if user_input:  #채팅창에 뭔가 입력하고 엔터를 눌렀을때 True가 됨
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # TODO (시즌2-2): 답변을 실시간 스트리밍으로 보여주고 싶다면 아래 3줄을
    #   with st.chat_message("assistant"):
    #       answer = st.write_stream(ask_stream(st.session_state.agent, user_input, st.session_state.thread_id))
    #   로 바꿔보기 (llm_client.py에 ask_stream 구현 먼저 필요)
    #   - st.write_stream()은 제너레이터를 받아서 글자를 하나씩 흘려보내며 화면에 그려주고,
    #     스트리밍이 끝나면 합쳐진 전체 텍스트를 반환해줌 -> 그 반환값을 answer로 쓰면 아래 로직 그대로 재사용 가능
    answer = ask(st.session_state.agent, user_input, st.session_state.thread_id)    #LLM 호출

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)

