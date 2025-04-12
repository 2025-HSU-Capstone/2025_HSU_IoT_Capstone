import json
from pathlib import Path
from app.models.models import EnvData

def insert_env_data(db):
    path = Path("data/env_data.json")
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        env = EnvData(**item)
        db.add(env)

    db.commit()
    print(f"✅ {len(items)}개의 EnvData가 저장되었습니다.")
