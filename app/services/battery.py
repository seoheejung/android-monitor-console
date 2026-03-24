# 현재 실행 환경 확인용
import os

# 로컬(psutil) 방식 import
from app.services.battery_psutil import get_battery_status_psutil

# Termux 방식 import
from app.services.battery_termux import get_battery_status_termux


def is_termux_environment() -> bool:
    """
    현재 실행 환경이 Termux인지 판별
    """

    # Termux 기본 홈 경로 확인
    return "com.termux" in os.path.expanduser("~")


def get_battery_status() -> tuple[int, bool]:
    """
    실행 환경에 따라 배터리 조회 방식 분기
    """

    # Termux면 termux-api 사용
    if is_termux_environment():
        return get_battery_status_termux()

    # 그 외 로컬 환경은 psutil 사용
    return get_battery_status_psutil()