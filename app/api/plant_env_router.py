from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.db_tables import PlantEnvProfile
import json  # ✅ 반드시 필요

from openai import OpenAI

import requests

# 🔒 main.py 또는 plant_env_router.py 최상단에 추가
import ssl
import os
os.environ.pop("SSL_CERT_FILE", None)  # 👈 문제 환경변수 제거
ssl._create_default_https_context = ssl._create_unverified_context


router = APIRouter()

# ✅ 요청 스키마
class PlantRequest(BaseModel):
    name: str


# ✅ GPT를 통해 식물 환경 기준 생성 함수
def generate_env_with_gpt(plant_name: str) -> dict:
    # ✅ GPT 키 설정
    client  = OpenAI(api_key="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")
    prompt = f"""
식물 "{plant_name}"을 건강하게 키우기 위한 환경 기준을 아래 형식으로 JSON으로 반환해 주세요.
각 항목의 값은 일반적인 평균 수치를 기준으로 하되, 현실적으로 존재해야 하며 단위를 포함하지 않습니다.

❗아래 형식 그대로 key와 구조를 유지하고, 반드시 "watering_duration_sec" 값은 숫자 3으로 고정해 주세요.  
❗설명 없이 JSON만 정확히 반환해 주세요.

형식 예시:
{{
  "temperature": {{ "min": int, "max": int }},
  "humidity": {{ "min": int, "max": int }},             // 적정 습도 범위 (%)
  "soil_moisture": {{ "min": int, "max": int }},        // 토양 습도 범위 (%)
  "light_cycle": {{
    "on": "HH:MM",                                     // 조명 시작 시간 (24시간 형식)
    "off": "HH:MM"                                     // 조명 종료 시간
  }},
  "watering_interval_hours": int,                      // 하루 몇 시간 간격으로 급수할지 (예: 8)
  "watering_duration_sec": 3,                         // 반드시 "watering_duration_sec" 값은 3으로 고정해 주세요. 
  "co2": int,
  "light": int                         // 1회 급수 시간 (초 단위, 예: 3)
}}

반드시 JSON만 출력해 주세요.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # 또는 gpt-4o
            messages=[
                {"role": "system", "content": "당신은 원예 전문가입니다."},
                {"role": "user", "content": prompt.strip()}
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        
        # ✅ 전처리: GPT가 ```json ... ``` 식으로 줄 수도 있어서 제거
        if content.startswith("```json"):
            content = "\n".join(content.split("\n")[1:-1])  # 맨 앞뒤 라인 제거

        print("✅ GPT 응답 내용 확인:", content)  # ← 디버깅용

        try:
            env_data = json.loads(content)
        except json.JSONDecodeError as e:
            print("❌ JSON 파싱 실패:", e)
            raise HTTPException(status_code=500, detail="GPT 응답이 유효한 JSON이 아님")

        return env_data
    except Exception as e:
        print("❌ GPT 생성 실패:", e)
        raise HTTPException(status_code=500, detail="GPT로 환경 기준 생성 실패")



# POST: 식물 환경 기준 생성 (GPT or 하드코딩)
@router.post("/plant/env-recommendation")
def set_env_for_plant(request: PlantRequest, db: Session = Depends(get_db)):
    plant_name = request.name.strip()

    # ✅ 이미 DB에 존재하면 저장하지 않음
    existing = db.query(PlantEnvProfile).filter_by(plant_name=plant_name).first()
    if existing:
        return {"message": f"{plant_name}의 환경 기준은 이미 저장되어 있습니다."}

    # ✅ STEP 1: GPT 또는 모델로 기준값 생성 (나중에 이 부분 활성화)
    # ✨ 예시: 나중에 여기에 LLM 또는 환경 생성 함수 연결
    env = generate_env_with_gpt(plant_name)
    if not env:
        raise HTTPException(status_code=500, detail="모델에서 기준값 생성 실패")
    # ✅ 여기! GPT 응답을 받은 직후 강제로 고정
    env["watering_duration_sec"] = 3
    
    print("✅ 덮어쓰기 완료: watering_duration_sec =", env["watering_duration_sec"])
    print("📦 최종 GPT env:", env)
    print("📦 필드 타입:", {k: type(v) for k, v in env.items()})

    # # ✅ STEP 2: 현재는 하드코딩 값으로 대체
    # env = PLANT_ENV_MAP.get(plant_name)
    # if not env:
    #     raise HTTPException(status_code=404, detail="해당 식물에 대한 환경 기준이 없습니다.")

    # ✅ STEP 3: DB에 저장
    # ✅ 필수 필드 검증
    required_keys = ["co2", "light"]
    missing = [key for key in required_keys if key not in env]
    if missing:
        raise HTTPException(status_code=500, detail=f"GPT 응답에 누락된 필드: {', '.join(missing)}")

    profile = PlantEnvProfile(
        plant_name=plant_name,
        temperature=(env["temperature"]["min"] + env["temperature"]["max"]) / 2,
        humidity=(env["humidity"]["min"] + env["humidity"]["max"]) / 2,
        co2=int(env["co2"]),  # GPT 응답엔 없음 → 기본값 또는 계산 필요
        light=int(env["light"]),  # light_cycle 기준 추정 필요
        soil_moisture=(env["soil_moisture"]["min"] + env["soil_moisture"]["max"]) / 2,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

     # ✅ 라즈베리파이로 전송
    try:
        # # ✅ 라즈베리파이 IP (로컬임시서버)
        RASPBERRY_PI_URL = "http://192.168.137.156:8000/set_env" #같은은 와이파이이
        send_data = {
            # "plant_name": plant_name,
            k: v for k, v in env.items()
            if k not in ["co2", "light"]
        }
        send_data["watering_duration_sec"] = 3  
        print("✅ 덮어쓰기 완료: watering_duration_sec =", send_data["watering_duration_sec"])
        r = requests.post(RASPBERRY_PI_URL, json=send_data)
        r.raise_for_status()
        print(f"✅ 라즈베리파이에 전송 완료: {r.status_code}")
    except Exception as e:
        print(f"❌ 라즈베리파이 전송 실패: {e}")


    return {
        "message": f"{plant_name}의 환경 기준이 저장되었습니다.",
        "profile": env,
        "source": "현재는 하드코딩, 나중에 모델 연동 예정"
    }

# GET: 해당 식물의 환경 기준 조회
@router.get("/plant/env-profile/{plant_name}")
def get_env_profile(plant_name: str, db: Session = Depends(get_db)):
    profile = db.query(PlantEnvProfile).filter_by(plant_name=plant_name.strip()).first()
    if not profile:
        raise HTTPException(status_code=404, detail="해당 식물의 환경 기준이 없습니다.")

    return {
        "plant_name": profile.plant_name,
        "temperature": profile.temperature,
        "humidity": profile.humidity,
        "co2": profile.co2,
        "light": profile.light,
        "soil_moisture": profile.soil_moisture
    }
