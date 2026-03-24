def build_state_message(battery: int, charging: bool, idle_minutes: int) -> tuple[str, str]:
    """
    상태 기반 메시지 생성
    """

    # 배터리 경고 상태 (최우선)
    if battery <= 20:
        return "warning", f"배터리가 {battery}%야. 경고 상태야."

    # 충전 중
    if charging:
        return "healing", "충전 중이야. 회복 상태야."

    # 장시간 미사용
    if idle_minutes >= 30:
        return "sleep", f"{idle_minutes}분 동안 입력이 없어. 잠든 상태야."

    # 일정 시간 미사용
    if idle_minutes >= 10:
        return "focus", "집중 상태 유지 중이야."

    # 기본 상태
    return "idle", "대기 상태야."


def build_environment_message(weather, air_quality) -> str:
    """
    날씨 / 공기질 기반 메시지 생성
    """

    if air_quality.get("us_aqi") is not None and air_quality["us_aqi"] > 100:
        return f"공기 상태가 {air_quality['air_text']}이야. 실내 대기를 권장할게."

    weather_text = weather.get("weather_text")

    if weather_text in ["약한 비", "비", "강한 비", "약한 소나기", "소나기", "강한 소나기"]:
        return "비가 오고 있어. 물 타입 분위기가 강해."

    if weather_text in ["약한 눈", "눈", "강한 눈"]:
        return "눈이 내리고 있어. 조용하고 차가운 분위기야."

    if weather_text in ["흐림", "부분적으로 흐림", "안개", "서리 안개"]:
        return f"지금 날씨는 {weather_text}이야. 차분하게 대기 중이야."

    return "환경 정보는 안정적이야."
