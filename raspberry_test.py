# test_receiver.py
import requests

test_env = {
    "plant_name": "상추",
    "temperature": 23.5,
    "humidity": 60.0,
    "co2": 420,
    "light": 7000,
    "soil_moisture": 65
}

try:
    r = requests.post("http://127.0.0.1:5001/receive-env", json=test_env)
    r.raise_for_status()
    print(f"✅ 응답 코드: {r.status_code}")
    print(f"✅ 응답 본문: {r.json()}")
except Exception as e:
    print(f"❌ 전송 실패: {e}")
