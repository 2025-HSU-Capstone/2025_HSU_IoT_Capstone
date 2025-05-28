#상대경로 저장 버전 -> firebase는 절대경로 photopath바꾸기기
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.db_tables import EnvData, PlantLog, GrowthData
# 🔹 STEP 3: 기준값 조회
from app.models.db_tables import PlantEnvProfile  
# 라즈베리파이에서 실행 (Python 예시)
from fastapi import Request

# # 라즈베리파이는 이 센서값들을 JSON으로 만들
# sensor_data = {
#     "temperature": 25.3,
#     "humidity": 60,
#     "light": 5800,
#     "soil_moisture": float,
#     "plant_height_cm": 5.6
# }
# 1. 라즈베리파이가 주기적으로 센서 측정
# requests.post("http://<FASTAPI서버_IP>:8000/trigger-env", json=sensor_data)
router = APIRouter()

@router.post("/upload_status")
async def upload_status(request: Request):
    body = await request.json()
    print("✅ 라즈베리파이로부터 상태 수신:", body)
    return {"message": "상태 수신 완료"}


class EnvSummary(BaseModel):
    temperature: float
    humidity: int 
    light: int
    soil_moisture: float
    plant_height_cm: float = 0.0  # ✅ 키 값 추가


#2.측정한 값을 서버의 /trigger-env에 자동 전송
@router.post("/trigger-env")
async def trigger_env_summary(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print("✅ 라즈베리파이로부터 수신된 JSON:", body)  # 👈 이 줄이 콘솔에 출력함
    
    # 여기서 수동으로 모델 검증
    try:
        data = EnvSummary(**body)
    except Exception as e:
        print("❌ Pydantic 검증 실패:", e)
        raise
    
    # 이후 로직에서 data.temperature 등 그대로 사용 가능
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
        light_level=data.light,
        soil_moisture=data.soil_moisture
    )
    db.add(env)
    db.commit()
    db.refresh(env)

    # plant_log에 연결
    log.env_id = env.id
    db.commit()

    # growth_data의 plant_height, height_diff 저장장
    last_growth = db.query(GrowthData).order_by(GrowthData.id.desc()).first()
    last_height = last_growth.plant_height if last_growth else 0.0  # None이면 0.0 취급
    height_diff = data.plant_height_cm - last_height

    new_growth = GrowthData(
        plant_height=data.plant_height_cm,
        height_diff=height_diff
    )
    db.add(new_growth)
    db.commit()
    db.refresh(new_growth)

    log.height_id = new_growth.id
    db.commit()

    # event 저장
    # ✅ 가장 마지막에 추가된 식물의 기준값 사용
    # 4.서버는 "마지막에 선택된 식물"의 기준값을 불러옴
    profile = db.query(PlantEnvProfile).order_by(PlantEnvProfile.id.desc()).first()

    # 5. 기준값과 센서값을 비교해서 이벤트 판단
    if not profile:
        log.event = "환경 기준 없음"
    else:
        messages = []

        if data.soil_moisture < profile.soil_moisture * 0.8:
            messages.append("수분 부족")
        if data.temperature > profile.temperature * 1.1:
            messages.append("고온 경고")
        if data.humidity < profile.humidity * 0.7:
            messages.append("습도 낮음")
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
