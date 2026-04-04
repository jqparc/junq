# backend/database.py (수정 후 최종 모습 확인)

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # 이 줄이 있어야 함
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_7IsL9uqoNDfZ@ep-jolly-king-a186m392-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ⭐ 이 부분이 빠져있을 확률이 높습니다! 꼭 확인하세요.
Base = declarative_base() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()