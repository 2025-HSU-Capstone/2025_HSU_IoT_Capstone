import os
import time
import subprocess
from datetime import datetime

# 저장 디렉토리
SAVE_DIR = "/home/pi/timelapse"
os.makedirs(SAVE_DIR, exist_ok=True)

# 총 촬영 횟수 및 간격 (초)
TOTAL_SHOTS = 48
INTERVAL_SEC = 3600  # 1시간

print("📸 Timelapse capture started...")

for i in range(TOTAL_SHOTS):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"img_{i:02d}_{timestamp}.jpg"
    save_path = os.path.join(SAVE_DIR, filename)

    try:
        # Camera capture command (for Camera Module 3 with libcamera)
        subprocess.run([
            "libcamera-still",
            "-o", save_path,
            "--width", "1280",  # 원하는 해상도 설정
            "--height", "720",
            "--nopreview"
        ], check=True)
        print(f"✅ Captured {filename}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Capture failed at {i}: {e}")

    if i < TOTAL_SHOTS - 1:
        time.sleep(INTERVAL_SEC)

print("📦 Timelapse capture completed.")
