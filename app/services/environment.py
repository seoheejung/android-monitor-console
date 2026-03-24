from datetime import datetime, timedelta

import app.core.state_store as store

from app.services.weather import get_weather
from app.services.air_quality import get_air_quality


def get_cached_env():
    """
    날씨 / 공기질 캐시 조회
    - 5분 이내면 기존 캐시 재사용
    - 캐시 없거나 만료되면 새로 조회
    """
    now = datetime.now()

    if store.CACHE["updated_at"] is None or (now - store.CACHE["updated_at"]) > timedelta(minutes=5):
        store.CACHE["weather"] = get_weather(store.DEVICE_LAT, store.DEVICE_LON)
        store.CACHE["air"] = get_air_quality(store.DEVICE_LAT, store.DEVICE_LON)
        store.CACHE["updated_at"] = now

    return store.CACHE["weather"], store.CACHE["air"]