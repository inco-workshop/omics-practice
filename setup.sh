#!/bin/bash
# === Multi-Omics Workshop 환경 설정 ===
# Codespace / devcontainer 첫 실행 시 자동 호출됩니다.

echo "=== 1/4 한글 폰트 설치 ==="
if command -v apt-get &>/dev/null; then
    # Codespaces 이미지의 만료된 GPG 키 레포 제거 (yarn 등)
    sudo rm -f /etc/apt/sources.list.d/yarn.list 2>/dev/null || true
    sudo apt-get update -qq 2>/dev/null
    sudo apt-get install -y -qq fonts-nanum fontconfig >/dev/null 2>&1
    sudo fc-cache -fv >/dev/null 2>&1
else
    # macOS / local
    FONT_DIR="$HOME/.local/share/fonts"
    mkdir -p "$FONT_DIR"
    if [ ! -f "$FONT_DIR/NanumGothic-Regular.ttf" ]; then
        curl -sL "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf" \
             -o "$FONT_DIR/NanumGothic-Regular.ttf"
        curl -sL "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Bold.ttf" \
             -o "$FONT_DIR/NanumGothic-Bold.ttf"
        fc-cache -fv "$FONT_DIR" 2>/dev/null || true
    fi
fi

echo "=== 2/4 Python 패키지 설치 ==="
pip install -q -r requirements.txt

echo "=== 3/4 Jupyter 커널 등록 ==="
python -m ipykernel install --user --name conda_omics --display-name "Python (Omics)"

echo "=== 4/4 matplotlib 폰트 캐시 초기화 ==="
# 기존 캐시 삭제 후 재생성 (새 폰트 강제 인식)
rm -rf ~/.cache/matplotlib 2>/dev/null || true
python -c "
import matplotlib.font_manager as fm
fm._load_fontmanager(try_read_cache=False)
nanum = [f for f in fm.fontManager.ttflist if 'nanum' in f.name.lower()]
print(f'  폰트 {len(fm.fontManager.ttflist)}개 등록 (Nanum: {len(nanum)}개)')
"

echo ""
echo "=== 설치 완료 ==="
echo "노트북에서 'Python (Omics)' 커널을 선택하세요."
