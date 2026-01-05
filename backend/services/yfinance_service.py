import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. 달러 인덱스 가져오기
def get_dollar_index_data(strn_date: str, end_date: str):
    ticker = "DX-Y.NYB"
    return _fetch_fill_and_slice(ticker, strn_date, end_date, "DXY")

# 2. 원달러 환율 가져오기
def get_usd_krw_data(start_date: str, end_date: str):
    ticker = "KRW=X"
    return _fetch_fill_and_slice(ticker, start_date, end_date, "USD_KRW")

# --- [공통 내부 함수] ---
# 똑같은 로직이 반복되니, 내부 함수로 하나 만들어두면 코드가 훨씬 고급스러워집니다.
def _fetch_fill_and_slice(ticker: str, strn_date: str, end_date: str, col_name: str):
    
    req_dt_strn = datetime.strptime(strn_date, "%Y%m%d")
    req_dt_end = datetime.strptime(end_date, "%Y%m%d")

    fetch_dt_strn = req_dt_strn - timedelta(days=10)
    # 데이터 다운로드
    df = yf.download(ticker, start=fetch_dt_strn, end=req_dt_end, auto_adjust=True, progress=False)
    
    if df.empty:
        return pd.DataFrame()
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None

    df = df[['Close']].rename(columns={'Close': col_name})

    full_indx = pd.date_range(start=fetch_dt_strn, end=req_dt_end, freq='D')
    df = df.reindex(full_indx)

    df[col_name] = df[col_name].ffill()

    df.index.name = 'Date'

    result_df = df.loc[req_dt_strn:req_dt_end].copy()

    return result_df

# --- [병합 함수도 인덱스 기준으로 변경] ---
def merge_data_by_index(df1, df2):
    # 인덱스(Date)가 서로 같으므로, 인덱스 기준으로 합칩니다.
    # left_index=True, right_index=True 옵션 사용
    merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')
    return merged

# --- 테스트 실행 ---
if __name__ == "__main__":
    start = "20240101" 
    end = "20240105"

    df_dx = get_dollar_index_data(start, end)
    df_krw = get_usd_krw_data(start, end)
    
    # 합치기
    final_df = merge_data_by_index(df_dx, df_krw)
    
    print("--- 결과 (Date가 인덱스인 상태) ---")
    print(final_df)