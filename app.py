import streamlit as st
import uuid
from llm_client import build_agent, ask
from llm_client import build_agent, ask, ask_stream

#사이드바 "새 대화 시작" 버튼
with st.sidebar:
    if st.button('새 대화 시작'):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

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

    with st.chat_message("assistant"):
        answer = st.write_stream(ask_stream(st.session_state.agent, user_input, st.session_state.thread_id))

    st.session_state.messages.append({"role": "assistant", "content": answer})

