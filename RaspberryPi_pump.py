import json
import serial
import time
import os
from datetime import datetime, timedelta

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

json_path = "env.json"
if not os.path.exists(json_path):
    raise FileNotFoundError(f"❌ {json_path} 파일이 존재하지 않습니다.")

with open(json_path, "r") as f:
    config = json.load(f)

temp_range = config["temperature"]
humi_range = config["humidity"]
soil_range = config["soil_moisture"]
light_on = config["light_cycle"]["on"]
light_off = config["light_cycle"]["off"]
watering_interval = timedelta(hours=config["watering_interval_hours"])
watering_duration = config.get("watering_duration_sec", 5)
last_watering_time = datetime.now() - watering_interval

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

send_command(f"WATER:{watering_duration}")
last_watering_time = datetime.now()

while True:
    now = datetime.now()

    if check_light_cycle():
        send_command("LIGHT_ON")
    else:
        send_command("LIGHT_OFF")

    send_command("READ_SENSOR")

    timeout = time.time() + 5
    while time.time() < timeout:
        if arduino.in_waiting:
            line = arduino.readline().decode(errors="ignore").strip()
            if not line:
                continue

            print(f"📩 아두이노 응답: {line}")

            if line.startswith("TEMP:"):
                try:
                    line = line.replace("TEMP:", "").replace("HUMI:", "").replace("SOIL:", "").replace("LIGHT:", "")
                    temp, humi, soil, light = map(float, line.split())

                    print(f"🌡 온도: {temp}°C → {'✅ 정상' if temp_range['min'] <= temp <= temp_range['max'] else '⚠️ 범위 벗어남'}")
                    print(f"💧 습도: {humi}% → {'✅ 정상' if humi_range['min'] <= humi <= humi_range['max'] else '⚠️ 범위 벗어남'}")
                    print(f"🌱 토양 수분: {soil} → {'✅ 정상' if soil_range['min'] <= soil <= soil_range['max'] else '⚠️ 범위 벗어남'}")
                    print(f"🔆 조도 (밝을수록 높음): {light}")
                except Exception as e:
                    print(f"❌ 파싱 오류: {e} - 원문: {line}")
                break
        time.sleep(0.1)

    if now - last_watering_time > watering_interval:
        send_command(f"WATER:{watering_duration}")
        last_watering_time = now

    time.sleep(60)
