import json, serial, time, requests
from datetime import datetime, timedelta

# ✅ env.json 불러오기
with open("env.json", "r", encoding="utf-8") as f:
    growth_conditions = json.load(f)

light_on = growth_conditions["light_cycle"]["on"]
light_off = growth_conditions["light_cycle"]["off"]
watering_interval = timedelta(hours=growth_conditions["watering_interval_hours"])
watering_duration = 3  # ✅ 서버가 어떤 값을 보내든 강제로 3초로 고정
soil_min = growth_conditions["soil_moisture"]["min"]
soil_max = growth_conditions["soil_moisture"]["max"]

# ✅ 아두이노 연결
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

last_watered = datetime.now() - watering_interval
saved_today = False

# ✅ 조명 ON/OFF 판단
def get_light_status():
    now = datetime.now().time()
    on = datetime.strptime(light_on, "%H:%M").time()
    off = datetime.strptime(light_off, "%H:%M").time()
    return "ON" if (on <= now < off if on < off else now >= on or now < off) else "OFF"

# ✅ 급수 주기 확인
def get_watering_status():
    return "DONE" if datetime.now() - last_watered <= watering_interval else "NEED"

# ✅ 아두이노 명령 전송
def send_command(cmd):
    arduino.write((cmd + "\n").encode())
    time.sleep(0.2)

# ✅ 센서 데이터 수신
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
                    print(f"❌ 센서 응답 파싱 오류: {line}")
    raise ValueError("❌ 센서 데이터를 수신하지 못했습니다.")

# ✅ DB 저장용 POST 요청 전송
def send_to_trigger_env(temp, humi, light, soil_percent):
    try:
        data = {
            "temperature": round(temp, 1),
            "humidity": round(humi),
            "light": light,
            "soil_moisture": round(soil_percent, 1)
        }
        response = requests.post("http://192.168.137.206:8000/trigger-env", json=data)
        response.raise_for_status()
        print("📤 trigger-env로 센서 상태 전송 완료")
    except Exception as e:
        print(f"❌ trigger-env 전송 실패: {e}")

# ✅ 메인 루프 시작
print("🌱 센서 제어 루프 시작")
while True:
    now = datetime.now()
    try:
        temp, humi, light, soil = read_sensor()
        soil_percent = soil  # 퍼센트값 그대로 사용

        print(f"🌾 현재 토양 습도: {soil_percent:.1f}%")

        # ✅ 조명 제어
        light_status = get_light_status()
        send_command(f"LIGHT_{light_status}")

        # ✅ 급수 판단
        if get_watering_status() == "NEED" and soil_percent < soil_min:
            print(f"🚿 물 주는 중... {watering_duration}초")
            send_command(f"WATER:{watering_duration}")
            last_watered = datetime.now()
            print("✅ 물주기 완료")

        # ✅ 21:05에 trigger-env로 상태 전송
        if now.hour == 21 and now.minute == 5 and not saved_today:
            send_to_trigger_env(temp, humi, light, soil_percent)
            saved_today = True

        # ✅ 다음날 다시 저장 가능하게 초기화
        if not (now.hour == 21 and now.minute == 5):
            saved_today = False

    except Exception as e:
        print(f"❌ 루프 오류: {e}")

    print("🔁 1분 루프 반복 중...")
    time.sleep(60)
