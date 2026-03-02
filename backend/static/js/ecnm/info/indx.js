const limit = 10;
let currnetPage = 1;

document.addEventListener("DOMContentLoaded", () => {
    // 1. 로그인 체크
    const token = localStorage.getItem('accessToken');
    // if (!token) {
    //     alert("로그인이 필요합니다.");
    //     window.location.href = '/login.html'; // 로그인 페이지로 이동
    //     return;
    // }

    // 2. 게시글 목록 불러오기 실행
    loadPosts(1);

    // 3. 등록 버튼 클릭 시 'submitPost' 함수 실행 연결
    // const btn = document.getElementById("submitBtn");
    // if (btn) {
    //     btn.addEventListener("click", submitPost);
    // }
});
// 게시글 목록 불러오기 함수
async function loadPosts(page) {
    const listDiv = document.getElementById('postList');

    if (!listDiv) {
        console.error("오류: HTML에서 'postList' ID를 찾을 수 없습니다.");
        return;
    }
    const skip = (page -1) * limit;
    try {
        const response = await fetch(`/ecnm/info/posts?skip=${skip}&limit=${limit}`);
        
        if (!response.ok) throw new Error("데이터 불러오기 실패");

        const posts = await response.json();

        currentPage = page;
        listDiv.innerHTML = ""; 

        if (posts.length === 0) {
            listDiv.innerHTML = "<tr><td colspan='5' class='empty-row'>등록된 게시글이 없습니다.</td></tr>";
            return;
        }

        //받아온 글 목록을 하나씩 화면에 그림
        posts.forEach(post => {
            const date = new Date(post.created_at).toLocaleDateString();
            const category = post.category ? post.category : '일반'; // category가 없을 경우 기본값
            
            // ★ 테이블 행(tr) 생성
            const row = `
                <tr>
                    <td>${post.id}</td>
                    <td>${escapeHtml(category)}</td>
                    <td class="text-left" style="cursor:pointer;" onclick="location.href='/ecnm/info/post/${post.id}'">
                        ${escapeHtml(post.title)}
                    </td>
                    <td>No.${post.owner_id}</td>
                    <td>${date}</td>
                </tr>
            `;
            listDiv.insertAdjacentHTML('beforeend', row);
        });
        //하단 페이징 버튼
        updatePaginationUI(posts.length);

    } catch (error) {
        //console.error(error);
        console.error("발생한 에러 상세:", error);
        listDiv.innerHTML = "<tr><td colspan='5' class='empty-row' style='text-align:center; color:red; padding:20px;'>오류가 발생했습니다.</td></tr>";
    }
}

function updatePaginationUI(fetchedCount) {
    const pagination = document.querySelector('.board-pagination');
    if (!pagination) return;

    let html = '';

    // [이전] 버튼
    if (currentPage > 1) {
        html += `<a href="#" class="page-btn" onclick="loadPosts(${currentPage - 1}); return false;">&laquo;</a>`;
    } else {
        html += `<span class="page-btn" style="color: #ccc; cursor: not-allowed;">&laquo;</span>`;
    }

    // [현재 페이지]
    html += `<a href="#" class="page-btn active" onclick="return false;">${currentPage}</a>`;

    // [다음] 버튼 (가져온 갯수가 limit과 같으면 다음 페이지가 있을 것으로 간주)
    if (fetchedCount === limit) {
        html += `<a href="#" class="page-btn" onclick="loadPosts(${currentPage + 1}); return false;">&raquo;</a>`;
    } else {
        html += `<span class="page-btn" style="color: #ccc; cursor: not-allowed;">&raquo;</span>`;
    }

    pagination.innerHTML = html;
}

// 보안을 위한 특수문자 변환 함수 (XSS 방지)
function escapeHtml(text) {
    if (!text) return "";
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}