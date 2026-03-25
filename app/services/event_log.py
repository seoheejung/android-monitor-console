from datetime import datetime

import app.core.state_store as store
from app.constants.state_profile import STATE_PROFILE

def add_event(event_type: str, message: str) -> None:
    """
    이벤트 로그 추가
    """
    now = datetime.now().strftime("%H:%M:%S")

    # 새 이벤트를 맨 앞에 추가
    store.EVENT_LOGS.insert(0, {
        "time": now,
        "type": event_type,
        "message": message,
    })

    # 최근 5개까지만 유지
    del store.EVENT_LOGS[5:]


def get_idle_minutes() -> int:
    """
    마지막 활동 시각 기준으로 유휴 시간(분) 계산
    """

    # 현재 시각과 마지막 활동 시간 차이 계산
    delta = datetime.now() - store.LAST_ACTIVITY_AT

    return int(delta.total_seconds() // 60)

def _get_state_label(state: str) -> str:
    """
    상태 key에 대응하는 UI label 반환
    """
    return STATE_PROFILE.get(state, STATE_PROFILE["idle"])["label"]

def _init_event_state(state: str, charging: bool, battery_warning: bool) -> None:
    """
    최초 1회 상태 초기화
    """
    if store.LAST_STATE is None:
        add_event("system", "Android Monitor Console 시작")
        add_event("state", f"시스템 상태 초기화: {_get_state_label(state)}")
        store.LAST_STATE = state

    if store.LAST_CHARGING is None:
        store.LAST_CHARGING = charging

    if store.LAST_BATTERY_WARNING is None:
        store.LAST_BATTERY_WARNING = battery_warning

def _handle_state_change(state: str) -> None:
    """
    상태 변경 감지 및 로그 기록
    """
    if store.LAST_STATE == state:
        return

    previous_label = _get_state_label(store.LAST_STATE)
    current_label = _get_state_label(state)

    add_event("state", f"상태 변경: {previous_label} → {current_label}")
    store.LAST_STATE = state


def _handle_charging_change(charging: bool) -> None:
    """
    충전 상태 변경 감지 및 로그 기록
    """
    if store.LAST_CHARGING is False and charging is True:
        add_event("power", "충전 시작")

    elif store.LAST_CHARGING is True and charging is False:
        add_event("power", "충전 해제")

    store.LAST_CHARGING = charging


def _handle_battery_warning_change(battery: int, battery_warning: bool) -> None:
    """
    배터리 경고 상태 변경 감지 및 로그 기록
    """
    if store.LAST_BATTERY_WARNING is False and battery_warning is True:
        add_event("battery", f"배터리 경고 진입: {battery}%")

    elif store.LAST_BATTERY_WARNING is True and battery_warning is False:
        add_event("battery", f"배터리 경고 해제: {battery}%")

    store.LAST_BATTERY_WARNING = battery_warning

def update_event_logs(state: str, battery: int, charging: bool) -> None:
    """
    상태 변화에 따라 이벤트 로그 갱신
    - 상태 초기화
    - 상태 변경
    - 충전 시작/해제
    - 배터리 경고 진입/해제
    """
    battery_warning = battery <= 20

    _init_event_state(
        state=state,
        charging=charging,
        battery_warning=battery_warning,
    )

    _handle_state_change(state)
    _handle_charging_change(charging)
    _handle_battery_warning_change(battery, battery_warning)