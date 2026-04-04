document.addEventListener("DOMContentLoaded", async () => {
    // URL에서 ID 추출 (예: /ecnm_info/detail/5 -> 5)
    const pathSegments = window.location.pathname.split('/');
    const postId = pathSegments[pathSegments.length - 1];

    try {
        const response = await fetch(`/ecnm/info/read/${postId}`);
        if (!response.ok) throw new Error("게시글을 찾을 수 없습니다.");

        const post = await response.json();
        const categoryMap = {
            'A': '당잠사',
            'B': '퇴근요정',
            'C': '시장지표',
            'D': '공지사항'
        }

        document.getElementById('postCategory').innerHTML = categoryMap[post.category];
        document.getElementById('postTitle').innerHTML = post.title;
        document.getElementById('postOwner').innerHTML = `${post.owner.nickname}`;
        document.getElementById('postDate').innerHTML = new Date(post.created_at).toLocaleDateString();
        document.getElementById('postContent').innerHTML = post.content;
    } catch (error) {
        console.error(error);
        alert("데이터 로드 실패");
        location.href = "/ecnm/info";
    }
});

function goToUpdate() {
    // 1. 현재 URL에서 ID 추출 (예: /ecnm/info/detail/5 -> 5)
    const pathSegments = window.location.pathname.split('/');
    const postId = pathSegments[pathSegments.length - 1];

    // 2. 수정 페이지로 이동
    if (postId) {
        window.location.href = `/ecnm/info/update/${postId}`;
    } else {
        alert("게시글 정보를 찾을 수 없습니다.");
    }
}

async function deletePost() {
    // 1. 사용자에게 진짜 삭제할 건지 한 번 더 확인 (실수 방지)
    if (!confirm("정말로 이 게시글을 삭제하시겠습니까? 삭제 후에는 복구할 수 없습니다.")) {
        return; // 취소를 누르면 여기서 멈춤
    }

    // 2. 현재 URL에서 게시글 ID 추출 (goToEdit 함수와 동일한 방식)
    const pathSegments = window.location.pathname.split('/');
    const postId = pathSegments[pathSegments.length - 1];

    if (!postId) {
        alert("게시글 정보를 찾을 수 없습니다.");
        return;
    }

    try {
        // 3. 백엔드로 DELETE 요청 보내기
        const response = await fetch(`/ecnm/info/delete/${postId}`, {
            method: 'DELETE',
            // 만약 삭제 시 로그인이 필수라면 아래 헤더 주석을 풀고 토큰을 같이 보내주세요.
            /*
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
            }
            */
        });

        // 4. 결과 처리
        if (response.ok) {
            alert("게시글이 성공적으로 삭제되었습니다.");
            window.location.href = '/ecnm/info'; // 삭제 완료 후 목록 페이지로 이동
        } else {
            alert("삭제에 실패했습니다. (권한이 없거나 서버 오류)");
        }
    } catch (error) {
        console.error("삭제 중 오류 발생:", error);
        alert("서버와 통신 중 오류가 발생했습니다.");
    }
}