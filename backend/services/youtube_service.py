import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def save_youtube_text_bypass(url):
    print("🚀 '사람인 척'하는 브라우저를 실행합니다...")
    
    # undetected_chromedriver 초기화 (버전 체크 및 방지 우회 자동 적용)
    options = uc.ChromeOptions()
    # options.add_argument('--headless') # 처음엔 창을 띄워서(headless 주석처리) 확인하세요.
    
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        print(f"▶ 접속 성공: {url}")
        
        # [중요] 페이지가 완벽히 뜰 때까지 넉넉히 대기
        time.sleep(5) 

        print("⚠️ [안내] 30초 안에 브라우저에서 '스크립트 표시' 버튼을 직접 눌러주세요!")
        print("   (로그인이 필요하면 로그인 하셔도 됩니다. 막히지 않습니다.)")

        # 자막 텍스트가 로딩될 때까지 대기 (최대 30초)
        wait = WebDriverWait(driver, 30)
        # 자막 클래스(.segment-text)가 나타날 때까지 기다림
        segments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "segment-text")))
        
        if segments:
            print(f"✅ 자막 발견! ({len(segments)}줄)")
            
            full_text = []
            for segment in segments:
                text = segment.text.strip()
                if text:
                    full_text.append(text)
            
            # 파일로 저장
            filename = "subtitle_result.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(full_text)) # 줄바꿈으로 저장
                
            return f"✅ 저장 완료: {filename}"
        
    except Exception as e:
        return f"❌ 실패 (스크립트 버튼을 안 누르셨거나 로딩 실패): {e}"
        
    finally:
        print("🏁 브라우저 종료")
        driver.quit()

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=bvWsqTc6EkU"
    print(save_youtube_text_bypass(url))