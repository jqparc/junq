from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

# 1. 라우터 생성 (태그는 문서화용)
router = APIRouter(prefix="/ecnm", tags=["ecnm"])

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

nav_dtl_tab = [ 
    {"id": "idct", "name": "시장지표", "url": "/ecnm/idct"},
    {"id": "info", "name": "정보",     "url": "/ecnm/info"} 
] 

# 3. 홈 화면 연결
# HTML에서 url_for('home')라고 부르면 이 함수가 실행됩니다.
@router.get("/", name="ecnm")
def ecnm_indx(request: Request):
    # home.html을 브라우저에 보여줍니다.
    return templates.TemplateResponse("ecnm/ecnm_indx.html", {
        "request": request, 
        "active_top": "ecnm",  # 상단 탭 '홈'을 활성화 상태로 표시
        "active_dtl": "",  
        "nav_dtl_tabs": nav_dtl_tab
    })

@router.get("/idct", name="ecnm.idct")
def ecnm_idct(request: Request):
    # home.html을 브라우저에 보여줍니다.
    return templates.TemplateResponse("ecnm/ecnm_idct.html", {
        "request": request, 
        "active_top": "ecnm", 
        "active_dtl": "idct",  
        "nav_dtl_tabs": nav_dtl_tab
    })

@router.get("/info", name="ecnm.info")
def ecnm_info(request: Request):
    # home.html을 브라우저에 보여줍니다.
    return templates.TemplateResponse("ecnm/ecnm_info.html", {
        "request": request, 
        "active_top": "ecnm",  
        "active_dtl": "info", 
        "nav_dtl_tabs": nav_dtl_tab
    })