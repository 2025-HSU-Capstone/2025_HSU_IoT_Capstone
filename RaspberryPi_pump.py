import json
import serial
import time
import os
from datetime import datetime, timedelta

# ✅ 아두이노 포트 설정 (환경에 따라 수정)
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

# ✅ 환경 설정 파일 로드
json_path = "env.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"❌ {json_path} 파일이 존재하지 않습니다.")

with open(json_path, "r") as f:
    config = json.load(f)

# ✅ 생장 조건 파싱
temp_range = config["temperature"]
humi_range = config["humidity"]
soil_range = config["soil_moisture"]
light_on = config["light_cycle"]["on"]
light_off = config["light_cycle"]["off"]
watering_interval = timedelta(hours=config["watering_interval_hours"])
watering_duration = config.get("watering_duration_sec", 5)
last_watering_time = datetime.now() - watering_interval  # 첫 시작 시 급수 가능하게 설정

def check_light_cycle():
    now = datetime.now().time()
    on = datetime.strptime(light_on, "%H:%M").time()
    off = datetime.strptime(light_off, "%H:%M").time()
    if on < off:
        return on <= now < off
    else:
        return now >= on or now < off

def send_command(cmd):
    arduino.write((cmd + "\n").encode())
    print(f"🔁 명령 전송: {cmd}")
    time.sleep(0.3)

# ✅ 🚿 시작하자마자 급수 먼저 수행
send_command(f"WATER:{watering_duration}")
last_watering_time = datetime.now()

# ✅ 메인 루프
while True:
    now = datetime.now()

    # 1. 조명 제어
    if check_light_cycle():
        send_command("LIGHT_ON")
    else:
        send_command("LIGHT_OFF")

    # 2. 센서 값 요청
    send_command("READ_SENSOR")

    # 3. TEMP 응답 받을 때까지 최대 5초 대기
    timeout = time.time() + 5
    while time.time() < timeout:
        if arduino.in_waiting:
            line = arduino.readline().decode(errors="ignore").strip()
            if not line:
                continue

            print(f"📩 아두이노 응답: {line}")

            if line.startswith("TEMP:"):
                try:
                    line = line.replace("TEMP:", "").replace("HUMI:", "").replace("SOIL:", "")
                    temp, humi, soil = map(float, line.split())

                    print(f"🌡 온도: {temp}°C → {'✅ 정상' if temp_range['min'] <= temp <= temp_range['max'] else '⚠️ 범위 벗어남'}")
                    print(f"💧 습도: {humi}% → {'✅ 정상' if humi_range['min'] <= humi <= humi_range['max'] else '⚠️ 범위 벗어남'}")
                    print(f"🌱 토양 수분: {soil} → {'✅ 정상' if soil_range['min'] <= soil <= soil_range['max'] else '⚠️ 범위 벗어남'}")
                except Exception as e:
                    print(f"❌ 파싱 오류: {e} - 원문: {line}")
                break
        time.sleep(0.1)

    # 4. 급수 여부 확인
    if now - last_watering_time > watering_interval:
        send_command(f"WATER:{watering_duration}")
        last_watering_time = now

    # 5. 1분 대기 후 반복
    time.sleep(60)
