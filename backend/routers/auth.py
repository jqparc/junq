from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

# 1. 라우터 생성 (prefix="/auth" 설정으로 주소 앞에 항상 /auth가 붙음)
router = APIRouter(prefix="/auth", tags=["auth"])

# 2. 템플릿 폴더 설정 (위와 동일)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 3. 로그인 페이지 연결
# HTML에서 url_for('auth.login_page')라고 부르면 실행됨
@router.get("/login", name="auth.login_page")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 4. 회원가입 페이지 연결
# HTML에서 url_for('auth.signup_page')라고 부르면 실행됨
@router.get("/signup", name="auth.signup_page")
def signup_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})