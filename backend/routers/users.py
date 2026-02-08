from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import database, schemas, crud, auth, models # 필요한 모듈 임포트

# main.py에서 app = FastAPI() 하던 것 대신, 여기서는 router를 씁니다.
router = APIRouter(
    prefix="/users",  # 이 라우터의 URL 앞에 자동으로 /users가 붙습니다. (선택사항)
    tags=["users"],   # 문서(Docs)에서 'users' 그룹으로 묶입니다.
)

# 회원가입 (기존 main.py에서 가져옴)
# 실제 주소: /users/register
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이름입니다.")
    return crud.create_user(db=db, user=user)

# 로그인 (기존 main.py에서 가져옴)
# 실제 주소: /users/login
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    # models.py 수정에 맞춰 user.password로 검증
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user