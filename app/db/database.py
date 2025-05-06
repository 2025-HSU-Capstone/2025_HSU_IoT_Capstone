from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# FastAPI에서 DB 세션을 생성하고 자동으로 닫아주는 역할
#->get_db()가 없으면 db 인스턴스를 못 받아서 DB 쿼리 자체가 불가능
#DB 연결을 안전하고 효율적으로 관리하기 위한 필수 도구
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ 정리하자면
# 초기엔 JSON도 DB도 자주 바뀌니까 유연하게 설계하고,
# 수정할 땐 “DB ↔ 모델 ↔ JSON ↔ API 코드” 네 가지를 같이 맞춰주면 돼.


