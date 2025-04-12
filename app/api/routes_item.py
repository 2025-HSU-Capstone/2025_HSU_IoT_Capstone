import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path

from app.database import get_db


router = APIRouter()

