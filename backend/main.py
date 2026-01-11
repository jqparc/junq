from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, auth, crud
from database import engine, get_db
from routers import users, posts

# 서버 실행 시 DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. CORS 미들웨어 설정 추가
# 프론트엔드(HTML/JS)에서 백엔드로 접속할 수 있게 허용해줍니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 모든 곳에서 접속 허용 (개발 단계용)
    allow_credentials=True,
    allow_methods=["*"],      # GET, POST 등 모든 방식 허용
    allow_headers=["*"],      # 모든 요청 헤더 허용
)
# ★ 핵심: 쪼개놓은 라우터들을 여기에 등록합니다.
app.include_router(users.router)
app.include_router(posts.router) 