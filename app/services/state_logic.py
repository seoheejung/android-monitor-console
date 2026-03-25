def build_state_message(battery: int, charging: bool, idle_minutes: int) -> tuple[str, str]:
    """
    상태 기반 시스템 메시지 생성
    """

    # 배터리 경고 상태 (최우선)
    if battery <= 20:
        return "warning", f"배터리 잔량 {battery}%"

    # 충전 중
    if charging:
        return "healing", "충전 중"

    # 장시간 미사용
    if idle_minutes >= 30:
        return "sleep", f"{idle_minutes}분 미사용"

    # 일정 시간 미사용
    if idle_minutes >= 10:
        return "focus", "입력 없음 상태"

    # 기본 상태
    return "idle", "정상 상태"