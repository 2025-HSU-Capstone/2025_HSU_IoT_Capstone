#ORM 테이블들 모음 #DB테이블 정의
#테이블 만들고 서버 키면 생김(중복x)
# ✅ db_tables.py (수정됨)
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class GrowthData(Base):
    __tablename__ = "growth_data"
    id = Column(Integer, primary_key=True, index=True)
    plant_height = Column(Float)
    height_diff = Column(Float)

class EnvData(Base):
    __tablename__ = "env_data"
    id = Column(Integer, primary_key=True, index=True)
    soil_moisture = Column(Integer)
    light_level = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    co2_level = Column(Integer)

class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)

class PlantLog(Base):
    __tablename__ = "plant_logs"
    id = Column(Integer, primary_key=True, index=True)
    log_date = Column(Date)
    height_id = Column(Integer, ForeignKey("growth_data.id"))
    env_id = Column(Integer, ForeignKey("env_data.id"))
    diary_id = Column(Integer, ForeignKey("diary_entries.id"))
    event = Column(String(255))
    day = Column(String(10))

    height = relationship("GrowthData")
    env = relationship("EnvData")
    diary = relationship("DiaryEntry")
    photos = relationship("Photo", back_populates="log", cascade="all, delete")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    photo_path = Column(Text)
    log_id = Column(Integer, ForeignKey("plant_logs.id"))

    log = relationship("PlantLog", back_populates="photos")

class PlantEnvProfile(Base):
    __tablename__ = "plant_env_profiles"

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String(100), unique=True, index=True)  # 예: "상추"
    temperature = Column(Float)
    humidity = Column(Float)
    co2 = Column(Integer)
    light = Column(Integer)
    soil_moisture = Column(Integer)