from app.models.db_tables import PlantLog, GrowthData, EnvData, Photo, DiaryEntry
from app.db.database import SessionLocal

db = SessionLocal()

from app.models.db_tables import PlantLog, GrowthData, EnvData, Photo, DiaryEntry
from app.db.database import SessionLocal

db = SessionLocal()

# 1️⃣ 모든 FK 끊기
logs = db.query(PlantLog).all()
for log in logs:
    log.photo_id = None
    log.env_id = None
    log.diary_id = None
    log.height_id = None
db.commit()  # 이걸 먼저 확실히 커밋해야 함!

photos = db.query(Photo).all()
for photo in photos:
    photo.log_id = None
db.commit()

# 2️⃣ FK 해제 후 삭제
for log in db.query(PlantLog).all():
    db.delete(log)
db.commit()

for photo in db.query(Photo).all():
    db.delete(photo)
for diary in db.query(DiaryEntry).all():
    db.delete(diary)
for g in db.query(GrowthData).all():
    db.delete(g)
for e in db.query(EnvData).all():
    db.delete(e)
db.commit()

print("✅ FK 해제 및 삭제 완료")

# PYTHONPATH=./ python seeders/reset.py