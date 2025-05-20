import json
import serial
import time
import os
from datetime import datetime, timedelta

# ✅ 아두이노 연결 (포트 이름은 실제 환경에 맞게 수정: /dev/ttyUSB0 or /dev/ttyACM0)
arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

# ✅ JSON 파일 경로 확인 및 로드
json_path = "env.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"❌ {json_path} 파일이 존재하지 않습니다.")

with open(json_path, "r") as f:
    config = json.load(f)

# ✅ 생장 조건 파싱
temp_range = config["temperature"]      # {"min": 20, "max": 30}
humi_range = config["humidity"]         # {"min": 50, "max": 70}
light_on = config["light_cycle"]["on"]  # 예: "07:00"
light_off = config["light_cycle"]["off"]# 예: "19:00"
watering_interval = timedelta(hours=config["watering_interval_hours"])
last_watering_time = datetime.now() - watering_interval  # 처음에 바로 급수 가능하게

def check_light_cycle():
    now = datetime.now().time()
    on = datetime.strptime(light_on, "%H:%M").time()
    off = datetime.strptime(light_off, "%H:%M").time()

    # 자정 넘어가는 경우 고려
    if on < off:
        return on <= now < off
    else:
        return now >= on or now < off

def send_command(cmd):
    arduino.write((cmd + "\n").encode())
    print(f"🔁 명령 전송: {cmd}")
    time.sleep(0.3)  # 아두이노 처리 여유 시간

# ✅ 메인 루프
while True:
    now = datetime.now()

    # ✅ 조명 ON/OFF
    if check_light_cycle():
        send_command("LIGHT_ON")
    else:
        send_command("LIGHT_OFF")

    # ✅ 급수 여부 확인
    if now - last_watering_time > watering_interval:
        send_command("WATER_ON")
        last_watering_time = now

    # ✅ 센서 값 요청
    send_command("READ_SENSOR")

    # ✅ 아두이노 응답 처리 (1줄만 읽기)
    if arduino.in_waiting:
        try:
            line = arduino.readline().decode().strip()
            if line.startswith("TEMP:"):
                # TEMP:25.3 HUMI:55.6 SOIL:684
                line = line.replace("TEMP:", "").replace("HUMI:", "").replace("SOIL:", "")
                temp, humi, soil = map(float, line.split())
                print(f"🌡 온도: {temp}°C, 💧 습도: {humi}%, 🌱 토양 수분: {soil}")

                # ✅ 조건 체크
                if not (temp_range["min"] <= temp <= temp_range["max"]):
                    print("⚠️ 온도 조절 필요")
                if not (humi_range["min"] <= humi <= humi_range["max"]):
                    print("⚠️ 습도 조절 필요")
        except Exception as e:
            print(f"❌ 파싱 오류: {e} - 원문: {line}")

    # ✅ 루프 주기 (1분마다 반복)
    time.sleep(60)
