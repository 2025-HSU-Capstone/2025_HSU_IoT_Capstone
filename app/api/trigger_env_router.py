#상대경로 저장 버전 -> firebase는 절대경로 photopath바꾸기기
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.db_tables import EnvData, PlantLog
# 🔹 STEP 3: 기준값 조회
from app.models.db_tables import PlantEnvProfile  
# 라즈베리파이에서 실행 (Python 예시)
import requests
# 라즈베리파이는 이 센서값들을 JSON으로 만들
sensor_data = {
    "temperature": 25.3,
    "humidity": 60,
    "co2": 410,
    "light": 5800,
    "soil_moisture": 42
}
# 1. 라즈베리파이가 주기적으로 센서 측정
# requests.post("http://<FASTAPI서버_IP>:8000/trigger-env", json=sensor_data)
router = APIRouter()

class EnvSummary(BaseModel):
    temperature: float
    humidity: float
    co2: int
    light: int
    soil_moisture: int

#2.측정한 값을 서버의 /trigger-env에 자동 전송
@router.post("/trigger-env")
def trigger_env_summary(data: EnvSummary, db: Session = Depends(get_db)):
    today = date.today()

    # 오늘 날짜의 log가 없으면 생성
    log = db.query(PlantLog).filter(PlantLog.log_date == today).first()
    if not log:
        log = PlantLog(log_date=today)
        db.add(log)
        db.commit()
        db.refresh(log)
    # 3. 서버는 센서값을 받아서 DB에 저장
    # env_data 저장
    env = EnvData(
        temperature=data.temperature,
        humidity=data.humidity,
        co2_level=data.co2,
        light_level=data.light,
        soil_moisture=data.soil_moisture
    )
    db.add(env)
    db.commit()
    db.refresh(env)

    # plant_log에 연결
    log.env_id = env.id
    db.commit()

    # event 저장
    # ✅ 가장 마지막에 추가된 식물의 기준값 사용
    # 4.서버는 "마지막에 선택된 식물"의 기준값을 불러옴
    profile = db.query(PlantEnvProfile).order_by(PlantEnvProfile.id.desc()).first()

    # 5. 기준값과 센서값을 비교해서 이벤트 판단
    if not profile:
        log.event = f"{data.plant_name}환경 기준 없음"
    else:
        messages = []

        if data.soil_moisture < profile.soil_moisture * 0.8:
            messages.append("수분 부족")
        if data.temperature > profile.temperature * 1.1:
            messages.append("고온 경고")
        if data.humidity < profile.humidity * 0.7:
            messages.append("습도 낮음")
        if data.co2 > profile.co2 * 1.2:
            messages.append("CO2 과다")
        if data.light < profile.light * 0.5:
            messages.append("광량 부족")
        # PlantLog.event에 event 저장
        log.event = ", ".join(messages) if messages else "환경 안정"

    db.commit()

    return {
        "message": "환경 데이터 저장 완료",
        "date": today.isoformat(),
        "env_id": env.id
    }
