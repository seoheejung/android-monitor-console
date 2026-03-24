# termux-api 명령 실행용
import subprocess
import json


def get_battery_status_termux() -> tuple[int, bool]:
    """
    Termux용 배터리 조회
    - termux-battery-status 명령 결과를 사용
    """

    try:
        # termux-battery-status 실행 결과 받기
        result = subprocess.check_output(["termux-battery-status"], text=True)

        # JSON 파싱
        data = json.loads(result)

        # 배터리 퍼센트 추출
        battery = int(data["percentage"])

        # 충전 상태 판별
        charging = data["status"] == "CHARGING"

        # 결과 반환
        return battery, charging

    # 실패 시 기본값 반환
    except Exception:
        return 100, False