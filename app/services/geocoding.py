import requests


def get_address(lat, lon):
    """
    좌표 → 주소 변환 (Reverse Geocoding)
    - OpenStreetMap Nominatim 사용
    """

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json",
                "zoom": 10
            },
            headers={
                "User-Agent": "PokeDesk/1.0"
            },
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

        address = data.get("address", {})

        city = (
            address.get("city")
            or address.get("municipality")
            or address.get("province")
            or address.get("state")
        )

        district = (
            address.get("city_district")
            or address.get("borough")
            or address.get("county")
            or address.get("suburb")
        )

        if city and district:
            return f"{city} {district}"

        if city:
            return city

        return "위치 정보 없음"

    except Exception as e:
        print("[get_address] 실패:", e)
        return "위치 정보 없음"