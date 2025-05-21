#상대경로 저장 버전 -> firebase는 절대경로 photopath바꾸기기
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import random
import os

from app.db.database import get_db
from app.models.db_tables import Photo, PlantLog, GrowthData

router = APIRouter()

@router.post("/upload-photo")
def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    now = datetime.now()
    today = now.date()
    current_hour = now.hour

    # ✅ 1. 이미지 저장 (로컬 images 폴더에 저장)
    save_dir = "images"
    os.makedirs(save_dir, exist_ok=True)
    filename = f"plant_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = os.path.join(save_dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ 2. plant_log 조회 또는 생성 (하루 1개)
    log = db.query(PlantLog).filter(PlantLog.log_date == today).first()
    if not log:
        log = PlantLog(log_date=today)
        db.add(log)
        db.commit()
        db.refresh(log)

    # ✅ 3. 사진 정보 DB에 저장 (상대경로로)
    relative_path = f"/images/{filename}"  # 👉 브라우저에서 접근 가능한 경로
    photo = Photo(photo_path=relative_path, log_id=log.id)
    db.add(photo)
    db.commit()

    # ✅ 4. 모델 예측 (현재는 더미로 랜덤)
    predicted_height = round(random.uniform(10.0, 25.0), 1)
    height_saved = False

    if current_hour == 12: #12시에 키 db에 저장(하루에 한번번)
        new_growth = GrowthData(plant_height=predicted_height, height_diff=0)
        db.add(new_growth)
        db.commit()
        db.refresh(new_growth)

        log.height_id = new_growth.id
        db.commit()
        height_saved = True

    return {
        "message": "사진 저장 완료",
        "photo_path": relative_path,
        "predicted_height": predicted_height,
        "height_saved": height_saved,
        "current_hour": f"{current_hour}시"
    }
