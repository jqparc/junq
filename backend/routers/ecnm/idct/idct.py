from fastapi import APIRouter, HTTPException
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from services import yfinance_service
import os

# 1. 라우터 생성 (태그는 문서화용)
router = APIRouter(prefix="/idct", tags=["idct"])

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/tbl/asset", name="ecnm.idct.assetTbl")
def get_asset_data_tbl(ticker: str, key: str):
    
    # # 두 값이 잘 들어왔는지 확인해봅니다.
    # print(f"요청받은 티커: {ticker}") # 출력: KRW=X
    # print(f"요청받은 키값: {key}")    # 출력: USD

    # yfinance 로직 처리 (여기에 key값을 활용한 로직을 추가하시면 됩니다)
    end_date = datetime.now()
    strn_date = end_date - timedelta(days=7)
    strn_chart = strn_date.strftime("%Y%m%d")
    end_chart  = end_date.strftime("%Y%m%d")

    yfTicker = yfinance_service.yf.Ticker(ticker)
    
    # 1. 일단 최근 5일치 데이터를 가져옵니다.
    hist = yfTicker.history(period="5d")

    # 2. 만약 명절 등 긴 연휴로 인해 5일치로도 2영업일 데이터가 안 나온다면?
    # -> 더 넉넉하게 한 달(1mo)치 데이터를 다시 가져와서 채웁니다.
    if len(hist) < 2:
        hist = ticker.history(period="1mo")

    # 3. 한 달치를 가져왔는데도 데이터가 아예 없는 경우 (상장 폐지, 잘못된 티커 등)
    if hist.empty:
        return {
            "current_price": 0.0,
            "prev_price": 0.0,
            "current_date": "N/A",
            "prev_date": "N/A"
        }
    
    # 5. 정상적으로 2영업일 이상 데이터가 있는 경우 (기존 정상 로직)
    latest_data = hist.iloc[-1]
    prev_data = hist.iloc[-2]

    thdy_price = round(float(latest_data['Close']), 2)
    prdy_price = round(float(prev_data['Close']), 2)

    current_date = latest_data.name.strftime('%Y-%m-%d')
    prev_date = prev_data.name.strftime('%Y-%m-%d')

    print(f"요청받은 티커: {current_date}") # 출력: KRW=X

    return {
        "status": "success",
        "ticker": ticker,
        key: {
            "clpr": thdy_price,
            "prdy_clpr": prdy_price,
            "prsn_date": current_date,
            "prdy_date": prev_date
        }
    }

@router.get("/cht/asset", name="ecnm.idct.assetCht")
def get_asset_data_cht(ticker: str, key: str):
    
    asset_map = {
        "dxy": {"ticker": "DX-Y.NYB", "key": "DXY"},    #달러인덱스
        "usd": {"ticker": "KRW=X", "key": "USD"},       #달러/원
        "btc": {"ticker": "BTC-USD", "key": "BTC"},     #비트코인
        "gld": {"ticker": "GC=F", "key": "GLD"},        #금
        "slv": {"ticker": "SI=F", "key": "SLV"},        #은
        "us3": {"ticker": "^IRX", "key": "US3"},        #미국 단기채(1-3)
        "u10": {"ticker": "^TNX", "key": "U10"},        #미국 10년물
        "u30": {"ticker": "^TYX", "key": "U30"},        #미국 30년물
        "wti": {"ticker": "CL=F", "key": "WTI"},        #WTI
        "spx": {"ticker": "^GSPC", "key": "SPX"},       #S&P500
        "nsq": {"ticker": "^IXIC", "key": "NSQ"},       #NASDAQ
        "dow": {"ticker": "^DJI", "key": "DOW"},        #DOWJONES
        "ksp": {"ticker": "^DJI", "key": "KSP"},        #KOSPI
        "ksq": {"ticker": "^KQ11", "key": "KSQ"},       #KOSDAQ
        "vix": {"ticker": "^VIX", "key": "VIX"},        #VIX
        "rss": {"ticker": "^RUT", "key": "RSS"}         #Russell 2000
    }
    
    # 소문자로 변환하여 매핑 딕셔너리에 있는지 확인
    # asset_info = asset_map.get(asset_type.lower())
    # if not asset_info:
    #     raise HTTPException(status_code=404, detail="지원하지 않는 지표입니다.")

    # 2. 공통 날짜 계산 로직
    end_date = datetime.now()
    strn_date = end_date - timedelta(days=365)
    strn_chart = strn_date.strftime("%Y%m%d")
    end_chart  = end_date.strftime("%Y%m%d")

    # 3. 데이터 가져오기 (asset_info 변수 활용)
    df = yfinance_service.get_yfinance_data(
        strn_chart, 
        end_chart, 
        ticker, 
        key
    )

    # 4. JSON 변환
    df = df.reset_index()
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    return df.to_dict(orient='records')