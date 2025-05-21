import ssl
import os

# ✅ SSL 인증서 문제 우회
os.environ.pop("SSL_CERT_FILE", None)
ssl._create_default_https_context = ssl._create_unverified_context


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

# ✅ 환경 변수 확인 (이 줄 추가!)
import os
print("🔍 ENV_HEADERS 관련 환경 변수:")
for k, v in os.environ.items():
    if 'HTTP' in k or 'PROXY' in k or 'LANG' in k or 'ENCOD' in k:
        print(f"{k} = {v}")

client = OpenAI(api_key=api_key, default_headers={"User-Agent": "smartparm-client"})

# ✅ 프롬프트 생성 함수
def generate_prompt(data):
     # ✅ 문자열로 들어온 값들을 다시 숫자로 변환
    height_today = float(data["height_today"])
    height_yesterday = float(data["height_yesterday"])
    delta_height = round(height_today - height_yesterday, 1)

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

7. **성장 단계 추정**  
- 센서 데이터를 바탕으로 현재 식물의 성장 단계를 추정해 주세요. (예: 씨앗, 묘목, 성장기, 개화기)

8. **event 발생**
- plant log의 event 를 바탕으로 주요이벤트: 어쩌고 로 표현 해 주세요

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
- 주요 이벤트: {data.get('event', '없음')}
---

한 문장이 끝나면 한 줄씩 개행해 주세요.
"""
    # ✅ 여기! prompt에 한글 들어가서 ascii 깨질 때를 대비해서 utf-8로 재인코딩
    return prompt  # utf-8 인코딩/디코딩 제거


# ✅ 전체를 함수로 래핑
def generate_diary_from_model(sensor_data: dict) -> str:
    # ✅ GPT 호출
    print("GPT 요청 payload")

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
    return diary_text
