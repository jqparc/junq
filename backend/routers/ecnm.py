from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from services import yfinance_service
import os

# 1. 라우터 생성 (태그는 문서화용)
router = APIRouter(prefix="/ecnm", tags=["ecnm"])

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

nav_dtl_tab = [ 
    {"id": "idct", "name": "시장지표", "url": "/ecnm/idct"},
    {"id": "info", "name": "인사이트", "url": "/ecnm/info"} 
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

@router.get("/ecnm_idct", name="ecnm.ecnm_idct")
def get_ecnm_chart_data():
    end_date = datetime.now()
    strn_date = end_date - timedelta(days=365)

    strn_chart = strn_date.strftime("%Y%m%d")
    end_chart  = end_date.strftime("%Y%m%d")

    df_dxy = yfinance_service.get_dollar_index_data(strn_chart, end_chart)
    df_krw = yfinance_service.get_usd_krw_data(strn_chart, end_chart)

    df_merged = yfinance_service.merge_data_by_index(df_dxy, df_krw)
    df_merged = df_merged.fillna(method='ffill').fillna(method='bfill')

    df_reset = df_merged.reset_index()
    df_reset['Date'] = df_reset['Date'].dt.strftime('%Y-%m-%d')

    return df_reset.to_dict(orient= 'records')