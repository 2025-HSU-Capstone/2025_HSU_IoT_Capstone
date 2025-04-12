import json
from pathlib import Path
from app.models.models import GrowthData

def insert_growth_data(db):
    path = Path("data/growth_data.json")
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        growth = GrowthData(**item)
        db.add(growth)

    db.commit()
    print(f"✅ {len(items)}개의 GrowthData가 저장되었습니다.")
