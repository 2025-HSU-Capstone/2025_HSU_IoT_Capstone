from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.db.database import get_db
from app.models.db_tables import PlantLog, Photo
from io import BytesIO
from PIL import Image
import os
import requests
import cloudinary.uploader
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
import cv2
import numpy as np

# 📦 Cloudinary 설정
cloudinary.config(
    cloud_name="dawjwfi88",
    api_key="737816378397999",
    api_secret="P_JWtRHUKXXiy3MuGLzUpsBAADc"
)

router = APIRouter()

@router.get("/timelapse/date-range")
def get_timelapse_date_range(db: Session = Depends(get_db)):
    first_photo = db.query(Photo).order_by(Photo.id.asc()).first()
    last_photo = db.query(Photo).order_by(Photo.id.desc()).first()

    return {
        "start_date": first_photo.log.log_date if first_photo else None,
        "end_date": last_photo.log.log_date if last_photo else None,
    }

@router.get("/timelapse/video")
def generate_timelapse_with_music(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    

    # 1️⃣ DB에서 Cloudinary 이미지 URL 가져오기
    logs = (
        db.query(PlantLog)
        .filter(PlantLog.log_date.between(start_date, end_date))
        .order_by(PlantLog.log_date)
        .all()
    )

    image_urls = [photo.photo_path for log in logs for photo in log.photos]
    
    if not image_urls:
        return {"error": "해당 날짜 범위에 이미지가 없습니다."}

    # 2️⃣ Cloudinary 이미지 URL → OpenCV 이미지 객체 (메모리 처리)
    frames = []
    BASE_IMAGE_URL = "https://res.cloudinary.com/dawjwfi88/image/upload"
    
    for url in image_urls:
        if url.startswith("/"):
            url = BASE_IMAGE_URL + url

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            print(f"✅ 시도 중인 이미지 URL: {url}")
            print(f"📦 응답 Content-Type: {response.headers.get('Content-Type')}")
            print(f"📏 응답 바이트 길이: {len(response.content)}")

            img_array = np.frombuffer(response.content, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # moviepy는 RGB 포맷 필요
                frames.append(img_rgb)
            else:
                print(f"❌ OpenCV 디코딩 실패: {url}")
        except Exception as e:
            print(f"❌ 이미지 로드 실패: {url}")
            print(f"   ↳ 이유: {e}")
            continue

    # ✅ 프레임이 하나도 없으면 영상 생성 중단
    if len(frames) == 0:
        return {"error": "유효한 이미지가 없어 타임랩스 영상을 생성할 수 없습니다."}

    # 3️⃣ moviepy로 타임랩스 영상 생성
    clip = ImageSequenceClip(frames, fps=10)

    # 4️⃣ 음악 추가 (루트에 music.mp3가 있다고 가정)
    music_path = os.path.join("C:", "Users", "82103", "Desktop", "Iot", "backend", "app", "services", "timelapse", "music.mp3")
    if os.path.exists(music_path):
        try:
            audio = AudioFileClip(music_path)
            if clip.duration and audio.duration:
                loops = int(clip.duration // audio.duration) + 1
                audio_loop = concatenate_audioclips([audio] * loops).subclip(0, clip.duration)
                clip = clip.set_audio(audio_loop)
            else:
                print("⚠️ clip.duration or audio.duration 값이 유효하지 않음")
                clip = clip.set_audio(None)
        except Exception as e:
            print(f"⚠️ 음악 추가 실패: {e}")
            clip = clip.set_audio(None)
    else:
        clip = clip.set_audio(None)

    # 5️⃣ 영상 파일 저장
    now = datetime.now()
    filename = f"timelapse_{now.strftime('%Y%m%d_%H%M%S')}"
    temp_path = "temp_timelapse.mp4"
    video_buffer = BytesIO()

    try:
        clip.write_videofile(temp_path, codec="libx264", audio_codec="aac",  logger=None)
        with open(temp_path, "rb") as f:
            video_buffer.write(f.read())
        video_buffer.seek(0)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 6️⃣ Cloudinary 업로드
    upload_result = cloudinary.uploader.upload(
        file=video_buffer,
        folder="smartfarm/timelapse_video",
        public_id=filename,
        overwrite=True,
        resource_type="video"
    )
    cloudinary_url = upload_result["secure_url"]
    print("✅ 업로드 완료:", cloudinary_url)

    # 7️⃣ 결과 반환
    return {"video_url": cloudinary_url}
