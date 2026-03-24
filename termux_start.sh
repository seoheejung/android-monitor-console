#!/data/data/com.termux/files/usr/bin/bash

# 에러 발생 시 즉시 종료
set -e

echo "[1] 프로젝트 폴더 이동"
cd "$HOME/pokedesk"

echo "[2] 가상환경 활성화"
source venv/bin/activate

echo "[3] FastAPI 서버 실행"
echo "브라우저 접속 주소: http://127.0.0.1:8000"
echo "종료는 Ctrl + C"

uvicorn app.main:app --host 0.0.0.0 --port 8000