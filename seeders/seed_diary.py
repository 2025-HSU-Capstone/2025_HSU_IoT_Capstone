import json
from pathlib import Path
from app.models.models import DiaryEntry

def insert_diary_entries(db):
    path = Path("data/diary_entries.json")
    with open(path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    for item in entries:
        diary = DiaryEntry(content=item["content"])
        db.add(diary)

    db.commit()
    print(f"✅ {len(entries)}개의 DiaryEntry가 저장되었습니다.")
