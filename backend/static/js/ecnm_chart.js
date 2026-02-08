// static/js/ecnm_chart.js

document.addEventListener("DOMContentLoaded", async function() {
    const ctx = document.getElementById('marketChart').getContext('2d');
    const loadingDiv = document.getElementById('chartLoading');

    // HTML 요소 가져오기
    const elDate = document.getElementById('latestDate');
    const elDXY = document.getElementById('latestDXY');
    const elKRW = document.getElementById('latestKRW');

    // [1] 커스텀 플러그인 정의: 마우스 오버 시 세로선 그리기
    const verticalHoverLine = {
        id: 'verticalHoverLine',
        beforeDatasetsDraw(chart) {
            // 마우스가 올라가서 활성화된 요소(Tooltip)가 있는지 확인
            const activeElements = chart.tooltip.getActiveElements();
            
            if (activeElements && activeElements.length > 0) {
                const { ctx, chartArea: { top, bottom } } = chart;
                const x = activeElements[0].element.x; // 활성화된 포인트의 X좌표

                ctx.save();
                ctx.beginPath();
                ctx.lineWidth = 2;         // 선 두께 (굵게)
                ctx.strokeStyle = '#555';  // 선 색상 (진한 회색)
                // 점선 효과를 원하면 아래 주석 해제
                // ctx.setLineDash([5, 5]); 
                ctx.moveTo(x, top);
                ctx.lineTo(x, bottom);
                ctx.stroke();
                ctx.restore();
            }
        }
    };

    function formatChange(current, prev, isCurrency = false) {
        if (prev === undefined || prev === null) return "";

        const diff = current - prev;
        const diffAbs = Math.abs(diff);
        let sign = "";
        let className = "change-flat";

        if (diff > 0) {
            sign = "▲";
            className = "change-up";
        } else if (diff < 0) {
            sign = "▼";
            className = "change-down";
        } else {
            sign = "-";
        }

        // 소수점 처리 (환율/지수 모두 2자리로 통일)
        const diffStr = diffAbs.toFixed(2);
        
        return `<span class="change-value ${className}">(${sign} ${diffStr})</span>`;
    }

    try {
        // 1. 백엔드 API 호출 (데이터 가져오기)
        const response = await fetch('/ecnm/ecnm_idct'); // FastAPI 엔드포인트
        const data = await response.json();
        
        // 데이터가 준비되면 로딩 문구 숨김
        loadingDiv.style.display = 'none';
        
if (data && data.length > 0) {
            const lastData = data[data.length - 1]; // 오늘(최신)
            const prevData = data.length > 1 ? data[data.length - 2] : null; // 어제(이전)

            // 1. 날짜
            elDate.innerText = lastData.Date; 
            
            // 2. 달러 인덱스
            const dxyVal = parseFloat(lastData.DXY);
            const dxyPrev = prevData ? parseFloat(prevData.DXY) : null;
            
            // 값 표시
            let dxyHtml = dxyVal.toFixed(2);
            // 증감 표시 추가
            dxyHtml += formatChange(dxyVal, dxyPrev);
            
            elDXY.innerHTML = dxyHtml; // innerText 대신 innerHTML 사용 (태그 적용)
            
            // 3. 원달러 환율
            const krwVal = parseFloat(lastData.USD_KRW);
            const krwPrev = prevData ? parseFloat(prevData.USD_KRW) : null;

            // 값 표시 (천단위 콤마)
            let krwHtml = krwVal.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            // 증감 표시 추가
            krwHtml += formatChange(krwVal, krwPrev);

            elKRW.innerHTML = krwHtml;
        }
        
        // 2. 데이터 가공
        const labels = data.map(item => item.Date);
        const dxyData = data.map(item => item.DXY);
        const krwData = data.map(item => item.USD_KRW);

        // 3. 차트 그리기
        new Chart(ctx, {
            type: 'line',// [2] 위에서 만든 플러그인 등록
            plugins: [verticalHoverLine],
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '달러 인덱스',
                        data: dxyData,
                        borderColor: '#b41010', // 빨강
                        backgroundColor: '#b41010',
                        yAxisID: 'y-left',      // 왼쪽 축 사용
                        tension: 0.3,
                        pointRadius: 0,
                        borderWidth: 2
                    },
                    {
                        label: '원/달러 환율',
                        data: krwData,
                        borderColor: '#09008d', // 파랑
                        backgroundColor: '#09008d',
                        yAxisID: 'y-right',     // 오른쪽 축 사용
                        tension: 0.3,
                        pointRadius: 0,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            boxWidth: 25,    // 가로 길이 (적당히 짧게)
                            boxHeight: 2,    // 세로 높이 (얇은 선처럼 보이게 설정)
                            usePointStyle: false, // 동그라미(Point) 대신 선(Line) 형태 사용
                            
                        }
                    },
                    title: {
                        display: false,
                        text: '달러 인덱스 vs 원달러 환율 추이'
                    }
                },
                scales: {
                    // [왼쪽 Y축] 달러 인덱스
                    'y-left': {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: '달러 인덱스' },
                        grid: { color: '#f0f0f0' }
                    },
                    // [오른쪽 Y축] 원달러 환율
                    'y-right': {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: { display: true, text: '원/달러 환율' },
                        grid: { drawOnChartArea: false } // 격자 겹침 방지
                    },
                    x: {
                        grid :{
                            display: true,
                            drawOnChartArea: true,
                            color: '#e0e0e0'
                        },
                        ticks: {
                            autoSkip: true,
                            autoSkipPadding: 20,
                            maxRotation: 0,
                            source: 'auto'
                        },
                        afterBuildTicks: function(axis){
                            const labels = axis.chart.data.labels;
                            const newTicks = [];
                            let prevMonth = "";

                            labels.forEach((label, index) =>{
                                const currentMonth = label.substring(0, 7);
                                if(currentMonth !== prevMonth){
                                    if(index > 0){
                                        newTicks.push({value: index});
                                    }
                                    prevMonth = currentMonth
                                }
                            });
                            axis.ticks = newTicks;
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error("차트 로딩 실패:", error);
        loadingDiv.innerText = "데이터를 불러오는 데 실패했습니다.";
    }
});