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

형식 예시:
{{
  "temperature": float,          // 예: 24.0 (°C)
  "humidity": float,             // 예: 60.0 (%)
  "co2": int,                   // 예: 400 (ppm)
  "light": int,                // 예: 7000 (lux)
  "soil_moisture": int,         // 예: 70 (%)
  "watering_amount": int,     // 하루 급수량 (mL 단위, 예: 300)
  "light_hours": int          // 하루 조명 시간 (예: 12)
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
    print("📦 최종 GPT env:", env)
    print("📦 필드 타입:", {k: type(v) for k, v in env.items()})

    # # ✅ STEP 2: 현재는 하드코딩 값으로 대체
    # env = PLANT_ENV_MAP.get(plant_name)
    # if not env:
    #     raise HTTPException(status_code=404, detail="해당 식물에 대한 환경 기준이 없습니다.")

    # ✅ STEP 3: DB에 저장
    profile = PlantEnvProfile(
        plant_name=plant_name,
        temperature=float(env["temperature"]),
        humidity=float(env["humidity"]),
        co2=int(env["co2"]),
        light=int(env["light"]),
        soil_moisture=int(env["soil_moisture"]),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

     # ✅ 라즈베리파이로 전송
    try:
        # # ✅ 라즈베리파이 IP (로컬임시서버버)
        RASPBERRY_PI_URL = "http://127.0.0.1:5001/receive-env" 
        send_data = {
            # "plant_name": plant_name,
            **env
        }
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
