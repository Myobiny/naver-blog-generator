import requests
import os
import re
from dataclasses import dataclass


@dataclass
class RestaurantInfo:
    name: str
    category: str
    address: str
    phone: str
    description: str
    map_url: str
    source: str
    raw_data: dict


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def search_naver(restaurant_name: str) -> "list[RestaurantInfo]":
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    if not client_id or not client_secret:
        return []

    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {"query": restaurant_name, "display": 5, "sort": "random"}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        items = resp.json().get("items", [])
    except Exception:
        return []

    results = []
    for item in items:
        results.append(
            RestaurantInfo(
                name=_strip_html(item.get("title", "")),
                category=item.get("category", ""),
                address=item.get("roadAddress") or item.get("address", ""),
                phone=item.get("telephone", ""),
                description=item.get("description", ""),
                map_url=item.get("link", ""),
                source="naver",
                raw_data=item,
            )
        )
    return results


def search_kakao(restaurant_name: str) -> "list[RestaurantInfo]":
    api_key = os.getenv("KAKAO_REST_API_KEY")
    if not api_key:
        return []

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {
        "query": restaurant_name,
        "category_group_code": "FD6",  # 음식점
        "size": 5,
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        documents = resp.json().get("documents", [])
    except Exception:
        return []

    results = []
    for doc in documents:
        results.append(
            RestaurantInfo(
                name=doc.get("place_name", ""),
                category=doc.get("category_name", ""),
                address=doc.get("road_address_name") or doc.get("address_name", ""),
                phone=doc.get("phone", ""),
                description="",
                map_url=doc.get("place_url", ""),
                source="kakao",
                raw_data=doc,
            )
        )
    return results


def search_restaurant(restaurant_name: str) -> "list[RestaurantInfo]":
    """네이버 → 카카오 순으로 식당 정보를 수집합니다."""
    results = search_naver(restaurant_name)
    if not results:
        results = search_kakao(restaurant_name)
    return results
