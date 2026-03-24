import os

# 로컬(psutil) 방식 배터리
from app.services.battery_psutil import get_battery_status_psutil

# Termux 방식 배터리
from app.services.battery_termux import get_battery_status_termux


def is_termux():
    """
    현재 실행 환경이 Termux인지 판별
    """

    # Termux 환경 변수 기반 확인
    return "PREFIX" in os.environ and "com.termux" in os.environ.get("PREFIX", "")


def get_battery_status():
    """
    실행 환경에 따라 배터리 조회 방식 분기
    """

    try:
        # Termux면 termux-api 사용
        if is_termux():
            return get_battery_status_termux()

        # 로컬 환경
        return get_battery_status_psutil()

    except Exception:
        # 실패 시 fallback
        return 100, False