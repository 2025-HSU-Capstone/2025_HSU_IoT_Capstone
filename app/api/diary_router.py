# ✅ diary_router.py (전체 수정본)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.db_tables import PlantLog, GrowthData, EnvData, DiaryEntry, Photo
from app.services.diary_model import generate_diary_from_model

router = APIRouter()

# ✅ 최신 날짜만 조회
@router.get("/diary/latest-date")
def get_latest_date(db: Session = Depends(get_db)):
    latest_log = db.query(PlantLog).order_by(PlantLog.log_date.desc()).first()

    if not latest_log:
        raise HTTPException(status_code=404, detail="No logs found")

    return {"latest_date": latest_log.log_date.strftime("%Y-%m-%d")}

# ✅ plantlog.height_id, env_id 있는 날짜 리스트 반환
@router.get("/diary/available-dates")
def get_available_diary_dates(db: Session = Depends(get_db)):
    logs = db.query(PlantLog).filter(
        PlantLog.height_id.isnot(None),
        PlantLog.env_id.isnot(None)
    ).all()
    date_list = [log.log_date.strftime("%Y-%m-%d") for log in logs]
    return date_list

# ✅ 외부 요청이 왔을 때, DB에서 데이터 꺼내서 모델에 넘기고 자동 다이어리 생성 후 프론트에 반환
@router.get("/diary/auto/{date_str}")
def get_diary_json(date_str: str, db: Session = Depends(get_db)):

    # ✅ 날짜 문자열 → datetime 객체 변환
    try:
        log_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식은 YYYY-MM-DD여야 합니다.")

    # ✅ 날짜 포맷 문자열
    formatted_date = f"{log_date.year}년 {log_date.month}월 {log_date.day}일"  # ✅ Windows 호환

    # ✅ 해당 날짜의 plant_logs 조회
    log = db.query(PlantLog).filter(PlantLog.log_date == log_date).first()
    if not log:
        raise HTTPException(status_code=404, detail="해당 날짜의 로그가 없습니다.")

    # ✅ 요일 계산 (한글)
    day_kr = log.day or log_date.strftime("%A")
    day_map = {
        "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일",
        "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일", "Sunday": "일요일"
    }
    if day_kr in day_map:
        day_kr = day_map[day_kr]

    # ✅ 연결된 테이블(plant_logs)에서 센서, 키 정보 가져오기
    growth = db.get(GrowthData, log.height_id)
    env = db.get(EnvData, log.env_id)

    if not all([growth, env]):
        raise HTTPException(status_code=500, detail="센서 또는 키 데이터 누락")

    # ✅ 대표 사진 (있다면 1장만)
    photo = db.query(Photo).filter(Photo.log_id == log.id).first()  # ✅ log_id를 기준으로 대표 사진 1장 가져오기

    # ✅ diary 처리: 이미 있는 경우 vs 없는 경우 구분
    if log.diary_id:
        # ✅ 이미 다이어리 있는 경우 → 그냥 꺼내서 보여줌
        diary = db.get(DiaryEntry, log.diary_id)
        diary_text = diary.content
        already_saved = True
    else:
        # ✨ 나중에는 아래 주석 해제해서 모델 호출로 교체
        sensor_data = {
            "date": str(formatted_date),
            "day": str(day_kr),
            "height_today": str(round(growth.plant_height, 1)),
            "height_yesterday": str(round(growth.plant_height - growth.height_diff, 1)),
            "soil_moisture": str(env.soil_moisture),
            "temperature": str(env.temperature),
            "humidity": str(env.humidity),
            "event": str(log.event) 
        }

        # ✅ GPT 모델 호출
        diary_text = generate_diary_from_model(sensor_data)

        # ✅ DB에 다이어리 저장
        # growth_stage는 다이어리에 자연스럽게 저장되므로 따로 db저장 필요 x
        new_diary = DiaryEntry(content=diary_text)
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)

        # ✅ plant_logs에 diary_id 연결
        log.diary_id = new_diary.id
        db.commit()
        already_saved = False

    # ✅ 최종 JSON 응답
    return {
        "date": formatted_date,
        "day": day_kr,
        "sensor_data": {
            "date": formatted_date,
            "day": day_kr,
            "height_today": round(growth.plant_height, 1),
            "height_yesterday": round(growth.plant_height - growth.height_diff, 1),
            "soil_moisture": env.soil_moisture,
            "light": env.light_level,
            "temperature": env.temperature,
            "humidity": env.humidity,
            "co2": env.co2_level
        },
        "diary": diary_text,
        "photo_path": f"/{photo.photo_path.lstrip('/')}" if photo else None,
        "already_saved": already_saved  # ✅ 중복 생성 여부 반환
    }
