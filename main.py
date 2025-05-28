from fastapi import FastAPI
from datetime import datetime
from pathlib import Path

from app.db.database import engine, get_db
from app.models import db_tables
#라우터 호출
from app.api import timelapse_router
from app.api import growth_chart_router
from app.api import diary_router
from app.api import upload_photo_router
from app.api import trigger_env_router
from app.api import plant_env_router 

#프론트 요청 허용
from fastapi.middleware.cors import CORSMiddleware
#브라우저에 정적 파일 서빙
from fastapi.staticfiles import StaticFiles
import os

# orm 테이블들 db에에 테이블 생성 (이미 있으면 무시됨)
db_tables.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 정적 파일 서빙 (이미지 폴더)
app.mount("/images", StaticFiles(directory="images"), name="images")
# 🔸 images는 main.py 기준 상대경로야.

#CORSMi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # 또는 ["*"] 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 타임랩스 라우터 등록
app.include_router(timelapse_router.router)
#키변화그래프 라우터 등록
app.include_router(growth_chart_router.router)

app.include_router(diary_router.router)

app.include_router(upload_photo_router.router)

app.include_router(trigger_env_router.router)

app.include_router(plant_env_router.router) 


@app.get("/")
def root():
    return {"message": "SmartParm 백엔드 준비 완료!"}

# /images 경로로 정적 파일 서빙
app.mount(
    "/images",
    StaticFiles(directory=os.path.join(os.getcwd(), "images")),
    name="images"
)


#아나콘다로 가상환경 만들기
#아나콘다 모듈 설치 = 무조건 관리자권한 (아님 가상환경에 안 깔림)

# 그래서 재실행 시엔 이렇게만 하면 됨
# 
# cd /c/Users/82103/Desktop/사물인터넷/백엔드
# git push origin dev/backend

# uvicorn main:app --reload
# uvicorn main:app --host 0.0.0.0 --port 8000
# http://localhost:8000/docs
# http://localhost:8000/images/img_002.jpg
# http://192.168.137.206:8000/docs