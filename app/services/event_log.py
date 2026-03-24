from datetime import datetime

import app.core.state_store as store

def add_event(event_type: str, message: str) -> None:
    """
    이벤트 로그 추가
    """

    # 현재 시각 문자열 생성
    now = datetime.now().strftime("%H:%M:%S")

    # 새 이벤트를 맨 앞에 추가
    store.EVENT_LOGS.insert(0, {
        "time": now,
        "type": event_type,
        "message": message,
    })

    # 최근 10개까지만 유지
    del store.EVENT_LOGS[10:]


def get_idle_minutes() -> int:
    """
    마지막 활동 시각 기준으로 유휴 시간(분) 계산
    """

    # 현재 시각과 마지막 활동 시간 차이 계산
    delta = datetime.now() - store.LAST_ACTIVITY_AT

    # 초 → 분 변환
    return int(delta.total_seconds() // 60)

def update_event_logs(state: str, battery: int, charging: bool) -> None:
    """
    상태 변화에 따라 이벤트 로그 갱신
    - 상태 변경 시 로그 추가
    - 충전 시작/해제 시 로그 추가
    - 배터리 부족 진입 시 로그 추가
    """

    # 마지막 상태가 없으면 앱 시작 로그 추가
    if store.LAST_STATE is None:
        add_event("system", "PokeDesk 시작")
        add_event("state", f"init → {state}")
        store.LAST_STATE = state

    # 상태가 바뀌었으면 상태 변경 로그 추가
    if store.LAST_STATE != state:
        add_event("state", f"{store.LAST_STATE} → {state}")
        store.LAST_STATE = state

    # 마지막 충전 상태가 없으면 현재 값으로 초기화
    if store.LAST_CHARGING is None:
        store.LAST_CHARGING = charging

    # 충전 시작 감지
    if store.LAST_CHARGING is False and charging is True:
        add_event("power", "충전 시작")
        store.LAST_CHARGING = charging

    # 충전 해제 감지
    elif store.LAST_CHARGING is True and charging is False:
        add_event("power", "충전 해제")
        store.LAST_CHARGING = charging

    # 현재 배터리 부족 여부 계산
    battery_warning = battery <= 20

    # 마지막 배터리 경고 상태가 없으면 현재 값으로 초기화
    if store.LAST_BATTERY_WARNING is None:
        store.LAST_BATTERY_WARNING = battery_warning

    # 배터리 부족 상태 진입 감지
    if store.LAST_BATTERY_WARNING is False and battery_warning is True:
        add_event("battery", f"배터리 부족 진입: {battery}%")
        store.LAST_BATTERY_WARNING = battery_warning

    # 배터리 부족 상태 해제 감지
    elif store.LAST_BATTERY_WARNING is True and battery_warning is False:
        add_event("battery", f"배터리 경고 해제: {battery}%")
        store.LAST_BATTERY_WARNING = battery_warning