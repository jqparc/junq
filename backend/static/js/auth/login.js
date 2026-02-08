document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch('/users/login', { 
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            alert("로그인 성공!");
            window.location.href = '/';
        } else {
            alert("정보가 일치하지 않습니다.");
        }
    } catch (error) {
        console.error(error);
        alert("서버 연결 실패");
    }
});