from app.models.db_tables import Photo

def insert_photos(db):
    # 📷 Cloudinary URL이 하드코딩된 10개 더미 사진
    photos = [
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831000/smartfarm/photo_logs/plant_20250518_190000.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831001/smartfarm/photo_logs/plant_20250519_190500.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831002/smartfarm/photo_logs/plant_20250520_191000.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831003/smartfarm/photo_logs/plant_20250521_191500.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831004/smartfarm/photo_logs/plant_20250522_192000.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831005/smartfarm/photo_logs/plant_20250523_192500.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831006/smartfarm/photo_logs/plant_20250524_193000.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831007/smartfarm/photo_logs/plant_20250525_193500.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831008/smartfarm/photo_logs/plant_20250526_194000.jpg" },
        { "photo_path": "https://res.cloudinary.com/dawjwfi88/image/upload/v1747831009/smartfarm/photo_logs/plant_20250527_194500.jpg" }
    ]

    for item in photos:
        photo = Photo(photo_path=item["photo_path"])
        db.add(photo)

    db.commit()
    print(f"✅ {len(photos)}개의 Photo가 저장되었습니다.")
