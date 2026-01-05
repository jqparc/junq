from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, auth, crud
from database import engine, get_db

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

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이름입니다.")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="정보가 일치하지 않습니다.")
    
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}