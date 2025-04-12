import json
from pathlib import Path
from app.models.models import Photo

def insert_photos(db):
    path = Path("data/photos.json")
    with open(path, "r", encoding="utf-8") as f:
        photos = json.load(f)

    for item in photos:
        photo = Photo(photo_path=item["photo_path"])
        db.add(photo)

    db.commit()
    print(f"✅ {len(photos)}개의 Photo가 저장되었습니다.")
