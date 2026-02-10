"""공용 시각화 설정 — 한글 폰트 + matplotlib 스타일"""
import os, platform, warnings
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

warnings.filterwarnings('ignore')

def setup():
    """한글 폰트 자동 감지 및 matplotlib 스타일 설정"""
    system = platform.system()

    # seaborn 스타일을 먼저 적용 (font.family를 덮어쓰므로)
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.unicode_minus'] = False

    font_name = None

    if system == 'Darwin':  # macOS
        for name in ['Apple SD Gothic Neo', 'AppleGothic', 'Nanum Gothic']:
            if any(name.lower() in f.name.lower() for f in fm.fontManager.ttflist):
                font_name = name
                break

    elif system == 'Windows':
        font_name = 'Malgun Gothic'

    else:  # Linux / Codespaces
        import shutil, subprocess

        # matplotlib 폰트 캐시 삭제 후 재스캔
        cache_dir = os.path.expanduser('~/.cache/matplotlib')
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir, ignore_errors=True)
        fm._load_fontmanager(try_read_cache=False)

        # 고정 경로에서 Nanum 폰트 확인
        fixed_paths = [
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
            os.path.expanduser('~/.local/share/fonts/NanumGothic-Regular.ttf'),
        ]
        nanum_fonts = [p for p in fixed_paths if os.path.exists(p)]

        # 고정 경로에 없으면 시스템 전체 검색
        if not nanum_fonts:
            nanum_fonts = [f for f in fm.findSystemFonts() if 'anum' in f.lower()]

        # 그래도 없으면 자동 설치 시도
        if not nanum_fonts:
            try:
                subprocess.run(
                    ['sudo', 'apt-get', 'install', '-y', '-qq', 'fonts-nanum'],
                    capture_output=True, timeout=60
                )
                subprocess.run(['fc-cache', '-fv'], capture_output=True)
                fm._load_fontmanager(try_read_cache=False)
                nanum_fonts = [p for p in fixed_paths if os.path.exists(p)]
            except Exception:
                pass

        for path in nanum_fonts:
            try:
                fm.fontManager.addfont(path)
                prop = fm.FontProperties(fname=path)
                font_name = prop.get_name()
                break
            except Exception:
                continue

    if font_name:
        plt.rcParams['font.family'] = font_name
    else:
        plt.rcParams['font.family'] = 'DejaVu Sans'
        print("[경고] 한글 폰트를 찾지 못했습니다. bash setup.sh 를 실행하세요.")

    return plt.rcParams['font.family']
