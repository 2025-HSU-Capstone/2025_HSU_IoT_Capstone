import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#직접실행 경로설정-무시가능

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from seed_growth import insert_growth_data
from seed_env import insert_env_data
from seed_photos import insert_photos
from seed_diary import insert_diary_entries
from seed_logs import insert_plant_logs,  update_days_in_logs


# 필요하면 다른 seed 모듈도 추가

def run():
    db: Session = SessionLocal()

    # insert_growth_data(db)
    # insert_env_data(db)
    # insert_photos(db)
    # insert_diary_entries(db)
    #외래키 모음 루트 테이블
    #insert_plant_logs(db)
    update_days_in_logs(db)


    db.close()

if __name__ == "__main__":
    run()
