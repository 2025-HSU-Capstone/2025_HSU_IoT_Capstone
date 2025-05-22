import requests

url = 'http://192.168.200.109:5000/env'  # 서버 IP로 수정

try:
    response = requests.get(url)
    if response.status_code == 200:
        env_data = response.json()
        print("✅ 환경 설정 받음:", env_data)
        # 여기서 env_data를 사용해서 조건 판단 등 수행
    else:
        print(f"❌ 서버 오류: {response.status_code}")
except Exception as e:
    print(f"❌ 요청 실패: {e}")