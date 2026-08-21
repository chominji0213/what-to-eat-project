"""
카카오 로컬 API(키워드로 장소 검색) 호출 모듈.

weather_tool.py와 같은 역할: "맛집 데이터를 가져오는 작업"만 담당.
LLM/Tool Calling 로직(llm_client.py)에서는 get_restaurant(query)만 호출하면 됨.
"""
import os
import requests
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv()

# 상수 정의
BASE_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

def _parse_restaurants(documents: list[dict]) -> list[dict]:
    results = []
    for doc in documents:
        result = {
            "이름": doc["place_name"],
            "카테고리": doc["category_name"],
            "주소": doc["address_name"],
            "전화번호": doc.get("phone", "정보없음"),
            "링크": doc["place_url"],
        }
        results.append(result)

    return results


def get_restaurant(query: str) -> dict:
    """
    지역/음식종류로 이루어진 검색어를 받아, 상위 몇 개의 음식점 정보를 정리해서 반환.
    LLM이 Tool Calling으로 호출할 함수.
    """
    if not KAKAO_API_KEY:
        return {"error": "KAKAO_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."}

    headers = {'Authorization': f'KakaoAK {KAKAO_API_KEY}'}
    params = {
        'query': query,
        'category_group_code': 'FD6',
        'size': 5
    }
    try:
        res = requests.get(BASE_URL, headers=headers, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        return {'error': f'Kakao API 호출 실패: {e}'}

    if not data['documents']:
        return {"error": f"'{query}'에 대한 검색 결과가 없습니다."}

    return {
        '검색어': query,
        '결과': _parse_restaurants(data['documents'])
    }
    
if __name__ == "__main__":
    # 터미널에서 python -m tools.restaurant_tool로 테스트
    print(get_restaurant("성수 퓨전한식"))
