#!/data/data/com.termux/files/usr/bin/bash

# 에러 발생 시 즉시 종료
set -e

echo "[1] 패키지 업데이트"
pkg update -y
pkg upgrade -y

echo "[2] Python / Git 설치"
pkg install python git -y

echo "[3] 저장소 권한 연결"
termux-setup-storage

echo "[4] 프로젝트 경로 확인"
PROJECT_DIR="$HOME/pokedesk"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "프로젝트 폴더가 없습니다: $PROJECT_DIR"
    echo "먼저 git clone 하거나 폴더를 복사해 주세요."
    exit 1
fi

echo "[5] 프로젝트 폴더 이동"
cd "$PROJECT_DIR"

echo "[6] 가상환경 생성"
if [ ! -d "venv" ]; then
    python -m venv venv
fi

echo "[7] 가상환경 활성화"
source venv/bin/activate

echo "[8] pip 업그레이드"
pip install --upgrade pip

echo "[9] requirements-termux 설치"
pip install -r requirements-termux.txt

echo "[완료] Termux 초기 설정 완료"
echo "다음부터는 ./termux_start.sh 로 실행하면 됩니다."