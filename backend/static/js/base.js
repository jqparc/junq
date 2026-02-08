
// 1. [공통] API 호출 함수 정의 (결과를 전역 변수에 저장)
// 이 코드가 실행되자마자 서버로 요청이 날아갑니다.
window.authRequest = (async function() {
    const token = localStorage.getItem("accessToken");
    if (!token) return null; // 토큰 없으면 바로 null 반환

    try {
        const response = await fetch("/users/me", {
            headers: { "Authorization": "Bearer " + token }
        });
        if (response.ok) {
            return await response.json(); // 성공 시 유저 정보 반환
        }
    } catch (error) {
        console.error("인증 실패:", error);
    }
    return null; // 실패하면 null 반환
})();

// 2. [공통] 상단 내비게이션 바 처리
// 위에서 만든 authRequest가 완료되길 기다렸다가 실행됩니다.
window.authRequest.then(user => {
    if (user) {
        // 로그인 상태 UI
        document.getElementById("auth-logged-in").style.display = "block";
        document.getElementById("auth-logged-out").style.display = "none";
        
        // 닉네임 표시
        const name = user.username;
        document.getElementById("user-name-display").innerText = name + "님";
    } else {
        // 로그아웃 상태 UI
        document.getElementById("auth-logged-in").style.display = "none";
        document.getElementById("auth-logged-out").style.display = "block";
    }
});

function logout() {
    localStorage.removeItem("accessToken");
    window.location.href = "/";
}