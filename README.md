# 🍜 오늘 뭐 먹지 추천봇

날씨 정보와 주변 맛집 검색을 결합한 Tool Calling 기반 추천 챗봇입니다.
사용자의 질문 의도에 따라 LLM이 필요한 도구를 스스로 선택하여 답변을 생성합니다.

## 개발 기간

2026.08 (개인 학습 프로젝트)

## 배포 링크

https://what-to-eat-project.onrender.com (Render 무료 플랜, 15분 미접속 시 슬립되어 재접속 시 로딩에 약 1분 소요될 수 있습니다)

## 사용 기술

`Python` `Streamlit` `LangChain` `LangGraph` `Google Gemini` `Docker`

- Language: Python
- Frontend: Streamlit
- LLM / Agent: LangChain (`create_agent`), LangGraph (`SqliteSaver`)
- 외부 API: 기상청 단기예보 API, 카카오 로컬 API
- Infra: Docker, Render

## 주요 기능

- 지역 기반 맛집 검색
- 지역별 실시간 날씨 조회
- 질문 맥락에 따라 하나 또는 여러 개의 도구를 조합해서 사용하는 Tool Calling 에이전트
- 서버가 재시작되어도 유지되는 대화 기록 (SQLite 기반 영구 저장)
- 답변이 실시간으로 타이핑되듯 나타나는 스트리밍 응답
- 사이드바 "새 대화 시작" 버튼으로 대화 초기화

## 프로젝트 구조

```
what-to-eat-project/
├── tools/
│   ├── weather_tool.py       # 날씨 API 연동
│   └── restaurant_tool.py    # 맛집 검색 API 연동
├── llm_client.py             # 에이전트 생성 및 Tool Calling 로직
├── app.py                    # Streamlit UI
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 실행 방법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경변수 설정 (.env.example 참고)
GOOGLE_API_KEY=
KMA_API_KEY=
KAKAO_API_KEY=

# 3. 실행
streamlit run app.py
```

### Docker로 실행

```bash
docker build -t what-to-eat-project .
docker run --env-file .env -p 8501:8501 what-to-eat-project
```

## 배운 점

- 여러 개의 Tool을 등록했을 때, LLM이 상황에 맞게 도구를 선택/조합하도록 프롬프트와 함수 설계를 구성하는 방법
- 인증 방식이 다른 두 개의 외부 API(쿼리 파라미터 방식, 헤더 방식)를 연동하는 방법
- LangGraph 체크포인터를 이용한 대화 상태 관리 (InMemorySaver → SqliteSaver로 전환하여 서버 재시작에도 대화 기록 유지)
- `agent.stream(stream_mode="messages")`로 토큰 단위 실시간 응답을 받아 Streamlit `st.write_stream()`으로 연결하는 방법
- Docker 기반 배포 및 클라우드 환경에서의 트러블슈팅
