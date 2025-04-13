from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json
from pathlib import Path

from app.database import engine, get_db
from app.models import models

# orm 테이블들 db에에 테이블 생성 (이미 있으면 무시됨)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SmartParm 백엔드 준비 완료!"}

#아나콘다로 가상환경 만들기
#아나콘다 모듈 설치 = 무조건 관리자권한 (아님 가상환경에 안 깔림)

# 그래서 재실행 시엔 이렇게만 하면 됨
# 
# cd /c/Users/82103/Desktop/사물인터넷/백엔드
# git push origin dev/backend