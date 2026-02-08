// frontend/js/register.js

let isNicknameChecked = false; // 닉네임 중복확인 통과 여부

// 닉네임 입력값이 변경되면 중복확인 상태 초기화
function resetNicknameCheck() {
    isNicknameChecked = false;
    const msgObj = document.getElementById('nickname-msg');
    if (msgObj) {
        msgObj.innerText = "";
    }
}

// 1. 닉네임 중복확인 함수
async function checkNickname() {
    const nicknameInput = document.getElementById('nickname');
    const nickname = nicknameInput.value;

    if (!nickname) {
        alert("닉네임을 입력해주세요.");
        return;
    }

    try {
        // 백엔드 API 주소 (환경에 맞게 수정 가능)
        const response = await fetch(`http://127.0.0.1:8000/check-nickname?nickname=${nickname}`);
        
        if (response.ok) {
            const data = await response.json();
            if (data.exists) {
                alert("이미 사용 중인 닉네임입니다.");
                isNicknameChecked = false;
                nicknameInput.focus();
            } else {
                alert("사용 가능한 닉네임입니다.");
                isNicknameChecked = true;
                const msgObj = document.getElementById('nickname-msg');
                if (msgObj) {
                    msgObj.innerText = "사용 가능합니다.";
                    msgObj.style.color = "green";
                }
            }
        } else {
            alert("서버 오류가 발생했습니다.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("서버 연결에 실패했습니다.");
    }
}

// 2. 회원가입 요청 함수 (handleRegister)
async function handleRegister() {

    // HTML의 input 요소들에서 값 가져오기
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const nickname = document.getElementById('nickname').value;
    const phone = document.getElementById('phone').value;

    // 간단한 유효성 검사
    if (!email || !username || !password || !nickname || !phone) {
        alert("모든 정보를 입력해주세요.");
        return;
    }

    // 닉네임 중복확인 여부 체크
    // if (!isNicknameChecked) {
    //     alert("닉네임 중복확인을 진행해주세요.");
    //     return;
    // }

    // 백엔드로 보낼 데이터 객체 생성
    const userData = {
        username: username,
        password: password,
        email: email,
        nickname: nickname,
        phone: phone
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            alert("회원가입 성공! 로그인 페이지로 이동합니다.");
            // 로그인 페이지로 리다이렉트 (경로는 프로젝트 상황에 맞게 조정)
            window.location.href = 'auth/login.html'; 
        } else {
            const errorData = await response.json();
            alert("회원가입 실패: " + (errorData.detail || "알 수 없는 오류"));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("서버와 통신 중 오류가 발생했습니다.");
    }
}