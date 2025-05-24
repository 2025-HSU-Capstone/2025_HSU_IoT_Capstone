import os
import cloudinary
import cloudinary.uploader

# Cloudinary 설정
cloudinary.config(
    cloud_name='dawjwfi88',
    api_key='737816378397999',
    api_secret='P_JWtRHUKXXiy3MuGLzUpsBAADc'
)

# 로컬 이미지 폴더 경로
local_folder = "app/services/timelapse/images"

# Cloudinary에 넣고 싶은 public_id 경로들 (파일명 포함)
cloudinary_public_ids = [
    f"smartfarm/photo_logs/plant_20250518_80000",
    f"smartfarm/photo_logs/plant_20250518_90000",
    f"smartfarm/photo_logs/plant_20250518_100000",
    f"smartfarm/photo_logs/plant_20250518_110000",
    f"smartfarm/photo_logs/plant_20250518_120000",
    f"smartfarm/photo_logs/plant_20250519_80000",
    f"smartfarm/photo_logs/plant_20250519_90000",
    f"smartfarm/photo_logs/plant_20250519_100000",
    f"smartfarm/photo_logs/plant_20250519_110000",
    f"smartfarm/photo_logs/plant_20250519_120000",
    f"smartfarm/photo_logs/plant_20250520_80000",
    f"smartfarm/photo_logs/plant_20250520_90000",
    f"smartfarm/photo_logs/plant_20250520_100000",
    f"smartfarm/photo_logs/plant_20250520_110000",
    f"smartfarm/photo_logs/plant_20250520_120000",
    f"smartfarm/photo_logs/plant_20250521_80000",
    f"smartfarm/photo_logs/plant_20250521_90000",
    f"smartfarm/photo_logs/plant_20250521_100000",
    f"smartfarm/photo_logs/plant_20250521_110000",
    f"smartfarm/photo_logs/plant_20250521_120000",
    f"smartfarm/photo_logs/plant_20250522_80000",
    f"smartfarm/photo_logs/plant_20250522_90000",
    f"smartfarm/photo_logs/plant_20250522_100000",
    f"smartfarm/photo_logs/plant_20250522_110000",
    f"smartfarm/photo_logs/plant_20250522_120000",
    f"smartfarm/photo_logs/plant_20250523_80000",
    f"smartfarm/photo_logs/plant_20250523_90000",
    f"smartfarm/photo_logs/plant_20250523_100000",
    f"smartfarm/photo_logs/plant_20250523_110000",
    f"smartfarm/photo_logs/plant_20250523_120000",
]

# 로컬 이미지 목록 (1.jpg ~ 30.jpg 기준)
local_images = sorted(os.listdir(local_folder))[:30]

# 매핑 업로드
# public_id가 "smartfarm/photo_logs/plant_20250518_80000"일 때
for i, filename in enumerate(local_images):
    local_path = os.path.join(local_folder, filename)
    full_public_id = cloudinary_public_ids[i]

    # ✅ 진짜 폴더/파일 이름 분리
    folder_path = "/".join(full_public_id.split("/")[:-1])        # smartfarm/photo_logs
    filename_only = full_public_id.split("/")[-1]                 # plant_20250518_80000

    print(f"📤 Uploading {filename} → {folder_path}/{filename_only}")

    with open(local_path, "rb") as f:
        result = cloudinary.uploader.upload(
            file=f,
            folder=folder_path,
            public_id=filename_only,
            overwrite=True,
            resource_type="image"
        )

    print(f"✅ 업로드 완료: {result['secure_url']}")
