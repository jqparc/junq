document.addEventListener("DOMContentLoaded", () => {
    //initializeTable();
    initGrid01();
    initGrid02();
    initCharts();
    //initCharts();
});
function initGrid01(){
    getyFinanceGrdData("KRW=X", "USD");        //달러/원
    getyFinanceGrdData("DX-Y.NYB", "DXY");     //달러인덱스
    getyFinanceGrdData("BTC-USD", "BTC");      //비트코인
    getyFinanceGrdData("ETH-USD", "ETH");      //이더리움
    getyFinanceGrdData("GC=F", "GLD");         //금
    getyFinanceGrdData("SI=F", "SLV");         //은
    getyFinanceGrdData("CL=F", "WTI");         //WTI유
    getyFinanceGrdData("^IRX", "US3");         //미국채1-3개월물
    getyFinanceGrdData("^TNX", "U10");         //미국채10년물
    getyFinanceGrdData("^TYX", "U30");         //미국채30년물
}
function initGrid02(){
    getyFinanceGrdData("^GSPC", "SNP");        //S&P 500
    getyFinanceGrdData("^IXIC", "NSQ");        //나스닥
    getyFinanceGrdData("^DJI", "DOW");         //다우존스
    getyFinanceGrdData("^KS11", "KSP");        //코스피
    getyFinanceGrdData("^KQ11", "KSQ");        //코스닥
    getyFinanceGrdData("^VIX", "VIX");         //빅스
    getyFinanceGrdData("^RUT", "RSS");         //러셀 2000
}
const chartConfigs = [
    { ticker: "DX-Y.NYB", key: "DXY", label: "Dollar Index",       color: "#e53935" },
    { ticker: "KRW=X",    key: "USD", label: "달러/원 환율",       color: "#e53935" },
    { ticker: "BTC-USD",  key: "BTC", label: "비트코인",           color: "#e53935" },
    { ticker: "ETH-USD",  key: "ETH", label: "이더리움",           color: "#e53935" },
    { ticker: "GC=F",     key: "GLD", label: "금",                 color: "#e53935" },
    { ticker: "SI=F",     key: "SLV", label: "은",                 color: "#e53935" },
    { ticker: "CL=F",     key: "WTI", label: "WTI유",              color: "#e53935" },
    { ticker: "^IRX",     key: "US3", label: "미국채 1-3개월물",   color: "#e53935" },
    { ticker: "^TNX",     key: "U10", label: "미국채 10년물",      color: "#e53935" },
    { ticker: "^TYX",     key: "U30", label: "미국채 30년물",      color: "#e53935" },
    { ticker: "^GSPC",    key: "SNP", label: "S&P 500",            color: "#e53935" },
    { ticker: "^IXIC",    key: "NSQ", label: "나스닥",             color: "#e53935" },
    { ticker: "^DJI",     key: "DOW", label: "다우존스",           color: "#e53935" },
    { ticker: "^KS11",    key: "KSP", label: "코스피",             color: "#e53935" },
    { ticker: "^KQ11",    key: "KSQ", label: "코스닥",             color: "#e53935" },
    { ticker: "^VIX",     key: "VIX", label: "VIX",                color: "#e53935" },
    { ticker: "^RUT",     key: "RSS", label: "러셀 2000",          color: "#e53935" }
];

// 2. async 함수로 변경하여 순차적으로 실행되게 만듭니다.
async function initCharts() {
    for (const config of chartConfigs) {
        await getyFinanceChtData(config.ticker, config.key, config.label, config.color);
    }
}
async function getyFinanceChtData(prTicker, prKey, prLabel, prColor){
    const ticker = prTicker; // 특수문자가 있어도 안전함!
    const key = prKey;
    const label = prLabel;
    const color = prColor;

    // 안전하게 인코딩해서 보내는 것이 좋습니다. (KRW%3DX 로 변환됨)
    const params = new URLSearchParams({
        ticker: ticker,
        key: key
    });

    try {
        // 3. fetch 주소 뒤에 ? 와 함께 조립된 파라미터를 붙여줍니다.
        const response = await fetch(`/ecnm/idct/cht/asset?${params.toString()}`);
        const data = await response.json();
        
        if (data && data.length > 0) {
            console.log(`${label} 데이터 로드 성공:`, data[0]); // 디버깅용 로그
            const chtid = 'chart' + key;
            drawChart(chtid, data, key, label, color);
        }
    } catch (error) {
        console.error("통신 에러:", error);
    }
}

async function getyFinanceGrdData(prTicker, prKey){
    const ticker = prTicker; // 특수문자가 있어도 안전함!
    const key = prKey;

    // 안전하게 인코딩해서 보내는 것이 좋습니다. (KRW%3DX 로 변환됨)
    const params = new URLSearchParams({
        ticker: ticker,
        key: key
    });
    console.log("생성된 파라미터:", params.toString());

    try {
        // 3. fetch 주소 뒤에 ? 와 함께 조립된 파라미터를 붙여줍니다.
        const response = await fetch(`/ecnm/idct/tbl/asset?${params.toString()}`);
        const data = await response.json();
        
        if (data && data.status ==="success") {
            const item = data[key];
            drawGrd(key, item);
        }
    } catch (error) {
        console.error("통신 에러:", error);
    }
}


function drawGrd(prkey, prData){
    const priceCell = document.getElementById(`cell-${prkey}`);
    const changeCell = document.getElementById(`cell-${prkey}-dif`);
    const dateCell = document.getElementById(`cell-${prkey}-date`);
    
    if(priceCell){
        priceCell.innerText = prData.clpr.toLocaleString('ko-KR', { minimumFractionDigits: 2 });
    }
    if(changeCell){
        const diff = prData.clpr - prData.prdy_clpr;
            const sign = diff >= 0 ? '+' : ''; // 양수면 + 표시
            
            changeCell.innerText = sign + diff.toLocaleString('ko-KR', { minimumFractionDigits: 2 });

            changeCell.style.color = diff >= 0 ? '#ff4d4f' : '#1890ff';
            changeCell.style.fontWeight = 'bold';
    }
    if(dateCell){
        console.log(dateCell);
        dateCell.innerText = prData.prsn_date + '\n(' + prData.prdy_date + ')'; 
        dateCell.style.fontSize = "0.7rem";
    }
}

function drawChart(canvasId, chartData, valueKey, labelText, lineColor) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // 공통 로직: 날짜 추출
    const labels = chartData.map(item => item.Date); 
    
    // 핵심 수정: 'DXY'나 'USD'처럼 하드코딩하지 않고, 전달받은 valueKey로 값을 추출합니다.
    const values = chartData.map(item => item[valueKey]); 

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: labelText,        // 넘겨받은 제목 사용
                data: values,            // 추출된 데이터 사용
                borderColor: lineColor,  // 넘겨받은 색상 사용
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                    title: {
                    display: true,
                    text: labelText, // ★ 전달받은 제목을 제목표시줄에 표시
                    // padding: { top: 10, bottom: 20 },
                    font: { size: 12, weight: 'bold' }
                },
                legend: {
                    display: false 
                }
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        drawBorder: false, // X축 바닥선 표시 여부 (취향에 따라 true/false)
                        
                        // 색상을 함수로 지정하여 특정 날짜에만 선을 그립니다.
                        color: function(context) {
                            // 데이터가 없거나 틱 정보가 없으면 투명 처리
                            if (!context.tick || context.tick.value === undefined) {
                                return 'transparent';
                            }

                            // 현재 틱의 인덱스로 날짜 문자열 가져오기
                            // (labels 변수는 상위 스코프에 있으므로 접근 가능)
                            const label = labels[context.tick.value];
                            if (!label) return 'transparent';

                            const parts = label.split('-');
                            const month = parseInt(parts[1], 10);
                            const day = parseInt(parts[2], 10);

                            // 1, 4, 7, 10월의 1일인 경우에만 회색 선 표시
                            if (day === 1 && [1, 4, 7, 10].includes(month)) {
                                return '#e0e0e0'; // 연한 회색 (원하는 색으로 변경 가능)
                            }
                            
                            // 그 외 날짜는 투명색 (선 안 보임)
                            return 'transparent';
                        }
                    },
                    
                    // ★ 핵심 수정: 틱(눈금) 글자 제어
                    ticks: {
                        // autoSkip: false, // 모든 라벨을 검사하도록 설정 (데이터가 너무 많으면 true로 두세요)
                        maxRotation: 0, // 글자 회전 방지
                        
                        callback: function(val, index) {
                            // 현재 그릴 라벨의 날짜 문자열을 가져옵니다 (예: "2024-01-01")
                            const label = this.getLabelForValue(val);
                            
                            // 문자열을 분석해서 월, 일을 추출
                            // "YYYY-MM-DD" 형식을 가정하고 '-'로 자릅니다.
                            const parts = label.split('-');
                            const month = parseInt(parts[1], 10);
                            const day = parseInt(parts[2], 10);

                            // 1월, 4월, 7월, 10월의 1일인 경우에만 라벨을 반환
                            if (day === 1 && [1, 4, 7, 10].includes(month)) {
                                return label; // "1/1", "4/1" 형태로 표시
                            }
                            
                            // 그 외의 날짜는 아무것도 표시하지 않음 (null 반환)
                            return null;
                        }
                    }
                },
                y: {
                    display: true
                }
            }
        }
    });
}