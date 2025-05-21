import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ✅ .env에서 API 키 불러오기
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY가 .env에 설정되어 있지 않습니다.")

client = OpenAI(api_key=api_key)

# ✅ 센서 데이터 예시
sensor_data = {
    "date": "2025년 5월 20일",
    "day": "화요일",
    "height_today": 23.4,
    "height_yesterday": 20.2,
    "soil_moisture": 35,
    "temperature": 23,
    "humidity": 57,
    "growth_stage": "성장기"   # 씨앗/묘목/성장기/개화기
}

# ✅ 프롬프트 생성 함수
def generate_prompt(data):
    delta_height = round(data["height_today"] - data["height_yesterday"], 1)

    prompt = f"""
다음은 스마트팜 식물의 센서 데이터입니다. 이 데이터를 기반으로 **자동 식물 성장일기**를 작성해 주세요. 적절히 이모티콘을 추가해도 좋습니다.
형식은 아래 예시처럼 자연스러운 일기 스타일을 유지하되, 다음 정보를 모두 자연스럽게 포함해야 합니다:

---

✅ 반드시 포함할 내용 (자연스럽게 녹여쓰기):

1. **기본 환경 정보**  
- 날짜 및 요일  
- 키 (전일 대비 변화 포함)  
- 토양 수분 (%)  
- 온도 / 습도  

2. **환경 평가**  
- 수분 상태 (적정 / 부족 / 과다)  
- 온습도 평가 (이상 없음 / 조절 필요 등)

3. **성장 요약**  
- 주요 성장 반응 (예: 키가 자람, 활발한 광합성 등)  
- 어제 대비 변화 요인 분석 (예: 온도 안정 → 성장 촉진)

4. **자동화 시스템 상태**  
- 자동 급수 시스템 작동 여부 (ON/OFF)  
- 조명 제어 시스템 작동 여부 (ON/OFF)

5. **관리 권장 사항**  
- 예: 수분 보충 필요, 습도 유지 등

6. **현재 성장 단계**  
- 예: "현재 식물은 성장기 단계입니다."

---

📝 작성 예시 (아래 형식대로 작성해주세요):

📅 2025년 5월 20일, 화요일 (자동 식물 성장 일기)

오늘의 식물 상태:
🌿 키(평균 높이): 23.4cm (어제 대비 +1.2cm)
💧 토양 수분 상태: 양호 (35%)
🌡️ 온도/습도: 23°C / 57% (이상 없음)

...

---

📊 센서 데이터:
- 날짜: {data['date']} ({data['day']})
- 키: {data['height_today']}cm (어제 {data['height_yesterday']}cm → +{delta_height}cm)
- 토양 수분: {data['soil_moisture']}%
- 온도: {data['temperature']}°C
- 습도: {data['humidity']}%
- 자동 급수 시스템: {data['water_system']}
- 조명 제어 시스템: {data['light_system']}
- 현재 성장 단계: {data['growth_stage']}

---

한 문장이 끝나면 한 줄씩 개행해 주세요.
"""
    return prompt

# ✅ GPT 호출
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "너는 스마트팜의 LLM 비서야. 친절하고 포멀하게 성장일기를 작성해줘."},
        {"role": "user", "content": generate_prompt(sensor_data)}
    ],
    temperature=0.7,
    max_tokens=700
)

# ✅ GPT 응답 텍스트
diary_text = response.choices[0].message.content

# ✅ JSON 데이터 구성
diary_data = {
    "date": sensor_data["date"],
    "day": sensor_data["day"],
    "sensor_data": sensor_data,
    "diary": diary_text
}

# ✅ 파일 저장 경로 구성
current_dir = os.path.dirname(__file__)
file_name = f"diary_{sensor_data['date'].replace('년 ','-').replace('월 ','-').replace('일','').replace(' ','')}.json"
json_file_path = os.path.join(current_dir, file_name)

# ✅ JSON 파일 저장
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(diary_data, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 파일로 저장 완료: {json_file_path}")



"""

# ✅ TXT 파일 저장 (일기 내용만)
txt_file_path = os.path.join(current_dir, file_name.replace('.json', '.txt'))
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(diary_text)

print(f"✅ TXT 파일로도 저장 완료: {txt_file_path}")

"""