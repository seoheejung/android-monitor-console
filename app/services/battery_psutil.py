# psutil 기반 배터리 조회
import psutil


def get_battery_status_psutil() -> tuple[int, bool]:
    """
    Windows / 일반 Linux용 배터리 조회
    - 배터리 정보가 없으면 기본값 반환
    """

    # psutil에서 배터리 정보 조회
    battery_info = psutil.sensors_battery()

    # 배터리 정보가 없으면 기본값 반환
    if battery_info is None:
        return 100, False

    # 배터리 퍼센트 추출
    battery = int(battery_info.percent)

    # 충전 여부 추출
    charging = bool(battery_info.power_plugged)

    # 결과 반환
    return battery, charging