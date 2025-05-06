from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.db_tables import PlantLog, Photo

router = APIRouter()

@router.get("/timelapse/date-range")
def get_timelapse_date_range(db: Session = Depends(get_db)):
    first_log = (
        db.query(PlantLog)
        .filter(PlantLog.photo_id != None)
        .order_by(PlantLog.log_date.asc())
        .first()
    )
    last_log = (
        db.query(PlantLog)
        .filter(PlantLog.photo_id != None)
        .order_by(PlantLog.log_date.desc())
        .first()
    )

    return {
        "start_date": first_log.log_date if first_log else None,
        "end_date": last_log.log_date if last_log else None,
    }


#지정한 날짜 범위 안에 있는 모든 사진을 날짜와 함께 JSON 형태로 반환 
# ->React: 이 json으로 리스트업해서 보여주면 끝끝
@router.get("/timelapse/images")
def get_timelapse_images(
    start_date: date = Query(..., description="2025-03-31"),
    end_date: date = Query(..., description="2025-04-09"),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(PlantLog)
        .filter(PlantLog.log_date.between(start_date, end_date))
        .order_by(PlantLog.log_date)
        .all()
    )

    photo_paths = []
    for log in logs:
        if log.photo_id:
            photo = db.query(Photo).filter(Photo.id == log.photo_id).first()
            if photo:
                photo_paths.append({
                    "date": log.log_date,
                    "path": f"/images/{photo.photo_path.split('/')[-1]}"
                })

    return {"images": photo_paths}
    

#응답 형태:
# {
#   "images": [
#     {
#       "date": "2025-04-02",
#       "path": "./images/img_002.jpg"
#     },
#     ...
#   ]
# }
