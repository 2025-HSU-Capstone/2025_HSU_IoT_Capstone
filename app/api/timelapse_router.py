from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.db_tables import PlantLog, Photo

router = APIRouter()

@router.get("/timelapse/date-range")
def get_timelapse_date_range(db: Session = Depends(get_db)):
    first_photo = db.query(Photo).order_by(Photo.id.asc()).first()
    last_photo = db.query(Photo).order_by(Photo.id.desc()).first()

    return {
        "start_date": first_photo.log.log_date if first_photo else None,
        "end_date": last_photo.log.log_date if last_photo else None,
    }

@router.get("/timelapse/images")
def get_timelapse_images(
    start_date: date = Query(...),
    end_date: date = Query(...),
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
        for photo in log.photos:
            photo_paths.append({
                "date": log.log_date,
                "path": f"/images/{photo.photo_path.split('/')[-1]}"
            })

    return {"images": photo_paths}
