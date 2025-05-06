from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.db_tables import PlantLog, GrowthData

router = APIRouter()

@router.get("/growth/date-range")
def get_growth_date_range(db: Session = Depends(get_db)):
    first_log = (
        db.query(PlantLog)
        .filter(PlantLog.height_id != None)
        .order_by(PlantLog.log_date.asc())
        .first()
    )
    last_log = (
        db.query(PlantLog)
        .filter(PlantLog.height_id != None)
        .order_by(PlantLog.log_date.desc())
        .first()
    )

    return {
        "start_date": first_log.log_date if first_log else None,
        "end_date": last_log.log_date if last_log else None,
    }
# 반환 결과 예시
# {
#   "start_date": "2025-04-01",
#   "end_date": "2025-04-09"
# }

#start_date, end_date를 받아서 그래프용 데이터를 JSON으로 반환해주는 API
@router.get("/growth/chart")
def get_growth_chart(
    start_date: date = Query(..., description="시작 날짜 (YYYY-MM-DD)"),
    end_date: date = Query(..., description="종료 날짜 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(PlantLog)
        .filter(PlantLog.log_date.between(start_date, end_date))
        .order_by(PlantLog.log_date)
        .all()
    )

    height_data = []
    for log in logs:
        if log.height_id:
            height = db.query(GrowthData).filter(GrowthData.id == log.height_id).first()
            if height:
                height_data.append({
                    "date": log.log_date,
                    "height": height.plant_height
                })

    return height_data


#응답 형태:
# [
#   { "date": "2025-04-01", "height": 12.3 },
#   { "date": "2025-04-02", "height": 12.7 },
#   ...
# ]
