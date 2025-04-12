from datetime import date, timedelta
from app.models.models import PlantLog, GrowthData, EnvData, DiaryEntry


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
            height_id=growth.id,
            env_id=env.id,
            photo_id=i,
            diary_id=diary.id,
            event=event
        )
        db.add(log)

    db.commit()
    print("✅ 10개의 PlantLog가 저장되었습니다.")
