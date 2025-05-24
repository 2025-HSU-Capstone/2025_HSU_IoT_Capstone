from app.models.db_tables import PlantLog, GrowthData, EnvData, Photo
from app.db.database import SessionLocal
from sqlalchemy import text
from datetime import date, timedelta
import random

db = SessionLocal()

db.execute(text("ALTER TABLE photos AUTO_INCREMENT = 1"))
db.execute(text("ALTER TABLE plant_logs AUTO_INCREMENT = 1"))
db.execute(text("ALTER TABLE growth_data AUTO_INCREMENT = 1"))
db.execute(text("ALTER TABLE env_data AUTO_INCREMENT = 1"))
db.commit()


base_date = date(2025, 5, 18)

for d in range(6):  # 6일
    day = base_date + timedelta(days=d)

    for i in range(5):  # 하루 5장
        timestamp = day.strftime("%Y%m%d") + f"_{8+i}0000"
        photo_path = f"https://res.cloudinary.com/dawjwfi88/image/upload/v1747834{d}{i}/smartfarm/photo_logs/plant_{timestamp}.jpg"

        if i == 0:
            # 로그 생성 (day, event, diary_id 비워둠)
            log = PlantLog(log_date=day)
            db.add(log)
            db.commit()
            db.refresh(log)

            # Growth
            height = round(12 + d * 0.5 + random.uniform(0.1, 0.5), 1)
            diff = round(random.uniform(0.3, 0.8), 1)
            growth = GrowthData(plant_height=height, height_diff=diff)
            db.add(growth)
            db.commit()
            db.refresh(growth)
            log.height_id = growth.id

            # Env
            env = EnvData(
                temperature=24 + random.uniform(-1, 3),
                humidity=60 + random.uniform(-10, 10),
                co2_level=390 + random.randint(0, 40),
                light_level=6000 + random.randint(-500, 500),
                soil_moisture=50 + random.randint(-20, 20)
            )
            db.add(env)
            db.commit()
            db.refresh(env)
            log.env_id = env.id

        # 사진 5장 등록 (모두 같은 log_id)
        photo = Photo(photo_path=photo_path, log_id=log.id)
        db.add(photo)
print("✅ db 저장 완료")
db.commit()