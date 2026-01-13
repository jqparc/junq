import os  # [수정 1] 운영체제 기능 불러오기
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models, schemas, auth, crud
from database import engine, get_db
from routers import users, posts, home, auth, ecnm
from starlette.middleware.sessions import SessionMiddleware

# 서버 실행 시 DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")
# [수정 2] 절대 경로 계산 (어디서 실행하든 폴더를 잘 찾게 해줌)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# [수정 3] 계산된 절대 경로(STATIC_DIR) 사용
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# [수정 4] 계산된 절대 경로(TEMPLATES_DIR) 사용
templates = Jinja2Templates(directory=TEMPLATES_DIR)


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
app.include_router(home.router)   # 홈 화면 (주소: /)
app.include_router(auth.router)   # 로그인/회원가입 (주소: /auth/...)
app.include_router(users.router)  # 유저 API
app.include_router(posts.router)  # 게시글 API
app.include_router(ecnm.router)  # 경제 화면 API