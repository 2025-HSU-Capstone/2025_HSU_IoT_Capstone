import os
import json
import serial
import time
import requests
import subprocess
import cloudinary
import cloudinary.uploader
from datetime import datetime, timedelta

# ✅ Cloudinary 설정
cloudinary.config(
    cloud_name="dawjwfi88",
    api_key="737816378397999",
    api_secret="P_JWtRHUKXXiy3MuGLzUpsBAADc"
)

# ✅ env.json 로딩
with open("env.json", "r", encoding="utf-8") as f:
    growth_conditions = json.load(f)

light_on = growth_conditions["light_cycle"]["on"]
light_off = growth_conditions["light_cycle"]["off"]
watering_interval = timedelta(hours=growth_conditions["watering_interval_hours"])
watering_duration = 3  # ✅ 항상 3초로 고정
soil_min = growth_conditions["soil_moisture"]["min"]
soil_max = growth_conditions["soil_moisture"]["max"]

# ✅ 아두이노 연결
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

save_dir = "/home/pi/timelapse"
os.makedirs(save_dir, exist_ok=True)
TRIGGER_URL = "http://192.168.137.206:8000/trigger-env"
PHOTO_UPLOAD_URL = "http://192.168.137.206:8000/upload_photo"

# ✅ 상태 변수 초기화
last_watered = datetime.now() - watering_interval
status_sent_today = False
last_photo_hour = -1
current_date = None
upload_count = 0

# ✅ 명령 전송 함수
def send_command(cmd):
    print(f"📤 아두이노로 명령 전송: {cmd}")
    arduino.write((cmd + "\n").encode())
    time.sleep(0.2)

# ✅ 센서 읽기 함수
def read_sensor():
    send_command("READ_SENSOR")
    for _ in range(10):
        if arduino.in_waiting:
            line = arduino.readline().decode().strip()
            if line.startswith("TEMP:"):
                try:
                    line = line.replace("TEMP:", "").replace("HUMI:", "").replace("SOIL:", "").replace("LIGHT:", "")
                    temp, humi, soil, light = map(float, line.split())
                    return temp, humi, int(light), soil
                except:
                    print(f"❌ 파싱 오류: {line}")
    raise ValueError("❌ 센서 응답 없음")

# ✅ 조명 제어 판단
def get_light_status():
    now = datetime.now().time()
    on = datetime.strptime(light_on, "%H:%M").time()
    off = datetime.strptime(light_off, "%H:%M").time()
    return "ON" if (on <= now < off if on < off else now >= on or now < off) else "OFF"

# ✅ 급수 간격 판단
def get_watering_status():
    return "DONE" if datetime.now() - last_watered <= watering_interval else "NEED"

# ✅ 키 측정 (YOLO)
def measure_plant_height():
    try:
        VENV_PYTHON = "/home/pi/plant_detect_project/venv/bin/python"
        DETECT_SCRIPT = "/home/pi/plant_detect_project/detect_plant.py"
        subprocess.run([VENV_PYTHON, DETECT_SCRIPT], check=True)

        height_file = "/home/pi/plant_detect_project/height.json"
        if os.path.exists(height_file):
            with open(height_file, "r") as f:
                data = json.load(f)
                return round(data["height_cm"], 2)
    except Exception as e:
        print(f"❌ 키 측정 오류: {e}")
    return None

# ✅ 상태 전송
def send_current_status(temp, humi, light, soil):
    try:
        height_cm = measure_plant_height()
        data = {
            "temperature": round(temp, 1),
            "humidity": int(humi),
            "light": int(light),
            "soil_moisture": round(soil, 1),
            "plant_height_cm": round(height_cm, 2) if height_cm else 0.0
        }

        with open("currentStatus.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        res = requests.post(TRIGGER_URL, json=data)
        res.raise_for_status()
        print("✅ 상태 전송 성공")

    except Exception as e:
        print(f"❌ 상태 전송 실패: {e}")

# ✅ 사진 촬영 + 업로드 + 서버 전송
def capture_and_upload_photo():
    global current_date, upload_count

    today_str = datetime.now().strftime("%Y%m%d")
    if current_date != today_str:
        current_date = today_str
        upload_count = 1
    else:
        upload_count += 1

    filename = f"photo_{today_str}_{upload_count:02d}.jpg"
    filepath = os.path.join(save_dir, filename)

    try:
        subprocess.run([
            "libcamera-still", "-o", filepath,
            "--width", "1280", "--height", "720", "--nopreview"
        ], check=True)
        print(f"📸 사진 촬영 완료: {filepath}")
    except Exception as e:
        print(f"❌ 사진 촬영 실패: {e}")
        return

    try:
        result = cloudinary.uploader.upload(
            filepath,
            folder="home/smartfarm/photo_logs",
            public_id=filename[:-4],
            overwrite=True,
            resource_type="image"
        )
        url = result["secure_url"]
        print(f"☁️ Cloudinary 업로드 성공: {url}")

        payload = {"photo_url": url}
        res = requests.post(PHOTO_UPLOAD_URL, json=payload)
        res.raise_for_status()
        print("✅ 서버로 이미지 URL 전송 완료")

    except Exception as e:
        print(f"❌ 업로드 또는 전송 실패: {e}")

# ✅ 루프 시작 전 → 첫 사진 촬영
print("🌿 RaspberryPi 센서 제어 루프 시작")
print("🖼️ 첫 실행 시 사진 1회 업로드 중...")
capture_and_upload_photo()
last_photo_hour = datetime.now().hour

# ✅ 메인 루프
while True:
    now = datetime.now()

    try:
        temp, humi, light, soil = read_sensor()
        print(f"🌡️ 온도={temp}, 습도={humi}, 조도={light}, 토양수분={soil:.1f}")

        send_command(f"LIGHT_{get_light_status()}")

        if get_watering_status() == "NEED":
            print("💧 항상 물 주기 작동 중...")
            send_command(f"WATER:{watering_duration}")
            last_watered = datetime.now()
            print("✅ 물 주기 완료")

        if now.hour == 20 and now.minute == 35 and not status_sent_today:
            print("📤 상태 자동 전송 중...")
            send_current_status(temp, humi, light, soil)
            status_sent_today = True
        if now.hour != 20 or now.minute != 35:
            status_sent_today = False

        if now.minute == 0 and now.hour != last_photo_hour:
            capture_and_upload_photo()
            last_photo_hour = now.hour

    except Exception as e:
        print(f"❌ 루프 오류: {e}")

    time.sleep(60)
