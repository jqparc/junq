    document.addEventListener("DOMContentLoaded", async () => {
        // URL에서 ID 추출 (예: /ecnm_info/detail/5 -> 5)
        const pathSegments = window.location.pathname.split('/');
        const postId = pathSegments[pathSegments.length - 1];

        try {
            const response = await fetch(`/ecnm/info/read/${postId}`);
            if (!response.ok) throw new Error("게시글을 찾을 수 없습니다.");

            const post = await response.json();

            document.getElementById('postCategory').innerHTML = post.category;
            document.getElementById('postTitle').innerHTML = post.title;
            document.getElementById('postOwner').innerHTML = `No.${post.owner_id}`;
            document.getElementById('postDate').innerHTML = new Date(post.created_at).toLocaleDateString();
            document.getElementById('postContent').innerHTML = post.content;
        } catch (error) {
            console.error(error);
            alert("데이터 로드 실패");
            location.href = "/ecnm/info";
        }
    });

    function goToEdit() {
        // 1. 현재 URL에서 ID 추출 (예: /ecnm/info/detail/5 -> 5)
        const pathSegments = window.location.pathname.split('/');
        const postId = pathSegments[pathSegments.length - 1];

        // 2. 수정 페이지로 이동
        if (postId) {
            window.location.href = `/ecnm/info/edit/${postId}`;
        } else {
            alert("게시글 정보를 찾을 수 없습니다.");
        }
    }