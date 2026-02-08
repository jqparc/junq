from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

# 1. 라우터 생성 (태그는 문서화용)
router = APIRouter(tags=["home"])

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 3. 홈 화면 연결
# HTML에서 url_for('home')라고 부르면 이 함수가 실행됩니다.
@router.get("/", name="home")
def home_index(request: Request):
    # home.html을 브라우저에 보여줍니다.
    return templates.TemplateResponse("home/home.html", {
        "request": request, 
        "active_top": "home",  # 상단 탭 '홈'을 활성화 상태로 표시
        "nav_dtl_tabs": []     # 하위 메뉴가 없어도 에러 안 나게 빈 리스트 전달
    })
