#ORM 테이블들 모음 #DB테이블 정의
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

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    photo_path = Column(Text)
   

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
    photo_id = Column(Integer, ForeignKey("photos.id"))
    diary_id = Column(Integer, ForeignKey("diary_entries.id"))
    event = Column(String(255))
    day = Column(String(10))


    height = relationship("GrowthData")
    env = relationship("EnvData")
    photo = relationship("Photo")
    diary = relationship("DiaryEntry")
