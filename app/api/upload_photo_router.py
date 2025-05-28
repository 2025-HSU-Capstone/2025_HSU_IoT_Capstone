# #상대경로 저장 버전 -> firebase는 절대경로 photopath바꾸기기
# import cloudinary
# import cloudinary.uploader
# from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime
# import shutil
# import random
# import os

# from app.db.database import get_db
# from app.models.db_tables import Photo, PlantLog, GrowthData

# router = APIRouter()
# # 1시간에 1번씩 옴 
# # 사진, 키값 반환 -> 12시에 오는 건 저장

# # ✅ 환경설정 추가 (보안상 .env로 분리 가능)
# cloudinary.config(
#     cloud_name='dawjwfi88',
#     api_key='737816378397999',
#     api_secret='P_JWtRHUKXXiy3MuGLzUpsBAADc'
# )

# @router.post("/upload-photo")
# def upload_photo(
#     file: UploadFile = File(...), 
#     db: Session = Depends(get_db),
#     predicted_height: float = 0.0,  # ✅ 라즈베리파이에서 보낸 키
# ):
#     now = datetime.now()
#     today = now.date()
#     current_hour = now.hour

#      # ✅ 1. Cloudinary 업로드
#     filename = f"plant_{now.strftime('%Y%m%d_%H%M%S')}"
#     folder = "smartfarm/photo_logs"
#     try:
#         upload_result = cloudinary.uploader.upload(
#             file.file,
#             folder=folder,
#             public_id=filename,  # ✅ 디렉토리 지정
#             overwrite=True,
#             resource_type="image"
#         )
#         cloudinary_url = upload_result['secure_url']
#         print("📁 실제 경로:", upload_result["public_id"])  
#         # 결과: "smartfarm/photo_logs/plant_20250521_214751"

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Cloudinary 업로드 실패: {str(e)}")
    
#     # # ✅ 1. 이미지 저장 (로컬 images 폴더에 저장)
#     # save_dir = "images"
#     # os.makedirs(save_dir, exist_ok=True)
#     # filename = f"plant_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
#     # file_path = os.path.join(save_dir, filename)

#     # with open(file_path, "wb") as buffer:
#     #     shutil.copyfileobj(file.file, buffer)

#     # ✅ 2. plant_log 조회 또는 생성 (하루 1개)
#     log = db.query(PlantLog).filter(PlantLog.log_date == today).first()
#     if not log:
#         log = PlantLog(log_date=today)
#         db.add(log)
#         db.commit()
#         db.refresh(log)

#     # ✅ 3. 사진 정보 DB에 저장 (상대경로로)
#     photo = Photo(photo_path=cloudinary_url, log_id=log.id)
#     db.add(photo)
#     db.commit()

#     # ✅ 대표 사진으로 지정 (첫 사진만)
#     if log.photo_id is None:
#         log.photo_id = photo.id
#         db.commit()

#     # # ✅ 4. 모델 예측 (현재는 더미로 랜덤)
#     # predicted_height = round(random.uniform(10.0, 25.0), 1)
#     # ✅ 5. 키 저장 조건 (12시에만)
#     height_saved = False

#     if current_hour == 12: #12시에 키 db에 저장(하루에 한번번)
#         new_growth = GrowthData(plant_height=predicted_height, height_diff=0)
#         db.add(new_growth)
#         db.commit()
#         db.refresh(new_growth)

#         log.height_id = new_growth.id
#         db.commit()
#         height_saved = True

#     return {
#         "message": "사진 저장 완료",
#         "photo_path": cloudinary_url,
#         "predicted_height": predicted_height,
#         "height_saved": height_saved,
#         "current_hour": f"{current_hour}시"
#     }


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.db_tables import Photo, PlantLog

router = APIRouter()

# ✅ 요청 JSON 스키마 정의
class PhotoRequest(BaseModel):
    photo_url: str

@router.post("/upload_photo")
def upload_photo(
    request: PhotoRequest,  # 📌 JSON 형식으로 받음
    db: Session = Depends(get_db),
):
    now = datetime.now()
    today = now.date()

    # 1. 오늘 날짜의 plant_log 조회 또는 생성
    log = db.query(PlantLog).filter(PlantLog.log_date == today).first()
    if not log:
        log = PlantLog(log_date=today)
        db.add(log)
        db.commit()
        db.refresh(log)

    # 2. Photo 테이블에 저장
    photo = Photo(photo_path=request.photo_url, log_id=log.id)
    db.add(photo)
    db.commit()

    # 3. 대표 사진이 아직 지정되지 않았으면 지정
    if log.photo_id is None:
        log.photo_id = photo.id
        db.commit()

    return {
        "message": "사진 경로 등록 완료",
        "photo_url": request.photo_url,
        "log_id": log.id,
        "is_representative": log.photo_id == photo.id
    }
