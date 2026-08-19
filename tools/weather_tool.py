"""
기상청 공공데이터포털 단기예보 API 호출 모듈.

이 파일은 "날씨 데이터를 가져오는 배관 작업"을 담당합니다.
LLM/Tool Calling 로직(llm_client.py)에서는 그냥 get_weather(city)만 호출하면 됩니다.
"""

import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
KMA_API_KEY = os.getenv("KMA_API_KEY")

BASE_TIMES = ["0200", "0500", "0800", "1100", "1400", "1700", "2000", "2300"]

# 지원 도시. 나중에 필요하면 여기에 도시만 추가하면 됨 (nx, ny)
CITY_TO_GRID = {
    "서울": (60, 127),
}

SKY_TEXT = {"1": "맑음", "3": "구름많음", "4": "흐림"}
PTY_TEXT = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}


def get_latest_base_datetime(now: datetime) -> tuple[str, str]:
    """
    현재 시각(now) 기준으로, 이미 조회 가능한(발표 후 10분 지난)
    가장 최근 base_date/base_time을 (문자열, 문자열) 튜플로 반환.
    """
    today_str = now.strftime("%Y%m%d")

    today_base_times = []
    for b in BASE_TIMES:
        base_dt = datetime.strptime(today_str + b, "%Y%m%d%H%M")
        today_base_times.append(base_dt)

    available = []
    for t in today_base_times:
        if t + timedelta(minutes=10) <= now:
            available.append(t)

    if available:
        latest = max(available)
    else:
        yesterday_str = (now.date() - timedelta(days=1)).strftime("%Y%m%d")
        latest = datetime.strptime(yesterday_str + "2300", "%Y%m%d%H%M")

    return latest.strftime("%Y%m%d"), latest.strftime("%H%M")


def _group_items_by_time(items: list[dict]) -> dict:
    """items 리스트를 (fcstDate, fcstTime) 기준으로 category:value 묶음으로 정리."""
    grouped = {}
    for item in items:
        key = (item["fcstDate"], item["fcstTime"])
        if key not in grouped:
            grouped[key] = {}
        grouped[key][item["category"]] = item["fcstValue"]
    return grouped


def get_weather(city: str) -> dict:
    """
    도시명을 받아 가장 가까운 시간대의 날씨를 정리해서 반환.
    LLM이 Tool Calling으로 호출할 함수.
    """
    if city not in CITY_TO_GRID:
        return {"error": f"'{city}'는 아직 지원하지 않는 도시입니다. 현재는 서울만 지원합니다."}

    if not KMA_API_KEY:
        return {"error": "KMA_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."}

    nx, ny = CITY_TO_GRID[city]
    now = datetime.now()
    base_date, base_time = get_latest_base_datetime(now)

    params = {
        "serviceKey": KMA_API_KEY,
        "numOfRows": 100,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    try:
        res = requests.get(BASE_URL, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        return {"error": f"기상청 API 호출 실패: {e}"}

    header = data.get("response", {}).get("header", {})
    if header.get("resultCode") != "00":
        return {"error": f"기상청 API 오류: {header.get('resultMsg')}"}

    items = data["response"]["body"]["items"]["item"]
    grouped = _group_items_by_time(items)

    if not grouped:
        return {"error": "예보 데이터가 비어 있습니다."}

    # 가장 가까운 미래 시간대 하나를 골라서 사람이 읽기 좋은 형태로 정리
    earliest_key = sorted(grouped.keys())[0]
    values = grouped[earliest_key]

    return {
        "도시": city,
        "날짜": earliest_key[0],
        "시각": earliest_key[1],
        "기온": f"{values.get('TMP', '정보없음')}도",
        "하늘상태": SKY_TEXT.get(values.get("SKY"), "정보없음"),
        "강수형태": PTY_TEXT.get(values.get("PTY"), "정보없음"),
        "강수확률": f"{values.get('POP', '정보없음')}%",
        "습도": f"{values.get('REH', '정보없음')}%",
    }


if __name__ == "__main__":
    # 터미널에서 python weather_tool.py로 테스트 하기 위함
    print(get_weather("서울"))
