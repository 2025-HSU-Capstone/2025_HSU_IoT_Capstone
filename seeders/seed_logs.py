from datetime import date, timedelta
from app.models.db_tables import PlantLog, GrowthData, EnvData, DiaryEntry, Photo


# 확장 가능성
# 나중에:
# event를 사용자가 직접 작성 가능하게
# event_logs 테이블 따로 만들어서 plant_log_id랑 1:N 관계로 관리 가능



def insert_plant_logs(db):
    today = date.today()

    for i in range(1, 11):
        growth = db.get(GrowthData, i)
        env = db.get(EnvData, i)
        diary = db.get(DiaryEntry, i)  # ✅ 추가된 부분
        photo = db.get(Photo, i)
        if not photo:
            continue  # 또는 예외 처리

        # ✅ 요일 계산 (한글)
        log_date = today - timedelta(days=10 - i)
        day_en = log_date.strftime("%A")
        day_kr = {
            "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일",
            "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일", "Sunday": "일요일"
        }[day_en]

        # 이벤트 조건 판단
        if growth.height_diff >= 0.7:
            event = "급성장 감지"
        elif env.soil_moisture < 30:
            event = "토양 수분 부족"
        elif env.co2_level > 420:
            event = "이산화탄소 농도 주의"
        elif "이상" in diary.content or "주의" in diary.content:
            event = "사용자 관찰 주의사항"
        else:
            event = "자동 센서 기록"

        log = PlantLog(
            log_date=today - timedelta(days=10 - i),
            day=day_kr,
            height_id=growth.id,
            env_id=env.id,
            photo_id=i,
            diary_id=diary.id,
            event=event
        )
        db.add(log)

    db.commit()
    print("✅ 10개의 PlantLog가 저장되었습니다.")

#요일만 추가해주는 함수-실제는 쓸모x
def update_days_in_logs(db):
    logs = db.query(PlantLog).all()
    for log in logs:
        if log.day:
            continue
        day_en = log.log_date.strftime("%A")
        log.day = {
            "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일",
            "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일", "Sunday": "일요일"
        }[day_en]
    db.commit()
    print("✅ 요일(day) 컬럼이 업데이트되었습니다.")

