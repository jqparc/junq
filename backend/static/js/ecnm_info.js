document.addEventListener("DOMContentLoaded", () => {
    // 1. 로그인 체크
    const token = localStorage.getItem('accessToken');
    // if (!token) {
    //     alert("로그인이 필요합니다.");
    //     window.location.href = '/login.html'; // 로그인 페이지로 이동
    //     return;
    // }

    // 2. 게시글 목록 불러오기 실행
    loadPosts();

    // 3. 등록 버튼 클릭 시 'submitPost' 함수 실행 연결
    // const btn = document.getElementById("submitBtn");
    // if (btn) {
    //     btn.addEventListener("click", submitPost);
    // }
});
// 게시글 목록 불러오기 함수
async function loadPosts() {
    const listDiv = document.getElementById('postList');

    if (!listDiv) {
        console.error("오류: HTML에서 'postList' ID를 찾을 수 없습니다.");
        return;
    }
    try {
        // 백엔드 라우터 주소 (/ecnm_info/posts)로 요청
        // const response = await fetch(`${API_BASE_URL}/ecnm/info/posts`);
        const response = await fetch('/ecnm_info/posts');
        
        if (!response.ok) throw new Error("데이터 불러오기 실패");

        const posts = await response.json();
        listDiv.innerHTML = ""; // 로딩 문구 지우기

        if (posts.length === 0) {
            listDiv.innerHTML = "<tr><td colspan='4' class='empty-row'>등록된 게시글이 없습니다.</td></tr>";
            return;
        }

        //받아온 글 목록을 하나씩 화면에 그림
        posts.forEach(post => {
            const date = new Date(post.created_at).toLocaleDateString();
            
            // ★ 테이블 행(tr) 생성
            const row = `
                <tr>
                    <td>${post.id}</td>
                    <td class="text-left" style="cursor:pointer;" onclick="location.href='/ecnm_info/post/${post.id}'">
                        ${escapeHtml(post.title)}
                    </td>
                    <td>No.${post.owner_id}</td>
                    <td>${date}</td>
                </tr>
            `;
            listDiv.insertAdjacentHTML('beforeend', row);
        });

    } catch (error) {
        //console.error(error);
        console.error("발생한 에러 상세:", error);
        listDiv.innerHTML = "<p style='color:red'>오류 발생</p>";
    }
}

// 보안을 위한 특수문자 변환 함수 (XSS 방지)
function escapeHtml(text) {
    if (!text) return "";
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}