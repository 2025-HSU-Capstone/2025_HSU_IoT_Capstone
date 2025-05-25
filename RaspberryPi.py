import json, serial, time, os
from datetime import datetime, timedelta

# ⬇️ 설정 로딩
env_path = "env.json"
with open(env_path, "r", encoding="utf-8") as f:
    growth_conditions = json.load(f)

light_on = growth_conditions["light_cycle"]["on"]
light_off = growth_conditions["light_cycle"]["off"]
watering_interval = timedelta(hours=growth_conditions["watering_interval_hours"])
watering_duration = growth_conditions["watering_duration_sec"]

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

last_watered = datetime.now() - watering_interval
saved_today = False

def get_light_status():
    now = datetime.now().time()
    on = datetime.strptime(light_on, "%H:%M").time()
    off = datetime.strptime(light_off, "%H:%M").time()
    return "ON" if (on <= now < off if on < off else now >= on or now < off) else "OFF"

def get_watering_status():
    return "DONE" if datetime.now() - last_watered <= watering_interval else "NEED"

def send_command(cmd):
    arduino.write((cmd + "\n").encode())
    time.sleep(0.2)

def read_sensor():
    send_command("READ_SENSOR")
    for _ in range(10):
        if arduino.in_waiting:
            line = arduino.readline().decode().strip()
            if line.startswith("TEMP:"):
                try:
                    line = line.replace("TEMP:", "").replace("HUMI:", "").replace("SOIL:", "").replace("LIGHT:", "")
                    temp, humi, soil, light = map(float, line.split())
                    return temp, humi, int(light), int(soil)  # soil, light는 정수로 변환
                except:
                    print(f"❌ 센서 응답 파싱 오류: {line}")
    raise ValueError("❌ 센서 데이터를 수신하지 못했습니다.")

while True:
    now = datetime.now()
    try:
        temp, humi, light, soil = read_sensor()

        # ⬇️ 조명 제어
        light_status = get_light_status()
        send_command(f"LIGHT_{light_status}")

        # ⬇️ 급수 제어
        if get_watering_status() == "NEED":
            print(f"🚿 물 주는 중... {watering_duration}초")
            send_command(f"WATER:{watering_duration}")
            last_watered = datetime.now()
            print("✅ 물주기 완료")

        # ⬇️ 21:05에 단순 JSON 저장
        if now.hour == 21 and now.minute == 5 and not saved_today:
            status = {
                "temperature": round(temp, 1),
                "humidity": round(humi),
                "light": light,
                "soil_moisture": soil
            }

            save_name = f"currentStatus_{now.strftime('%Y-%m-%d')}.json"
            with open(save_name, "w", encoding="utf-8") as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
            print(f"✅ 간단 상태 저장 완료: {save_name}")
            saved_today = True

        # ⬇️ 다음날 저장 가능하게 플래그 초기화
        if not (now.hour == 21 and now.minute == 5):
            saved_today = False

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    time.sleep(60)
