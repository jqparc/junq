
// ★ 에디터 실행 및 설정
var quill = new Quill('#editor-container', {
    theme: 'snow',
    placeholder: '내용을 입력하세요...',
    modules: {
        toolbar: [
            [{ 'header': [1, 2, 3, false] }],     // 제목 크기
            ['bold', 'italic', 'underline'],      // 굵게, 기울임, 밑줄
            [{ 'color': [] }, { 'background': [] }], // 글자색, 배경색
            [{ 'list': 'ordered'}, { 'list': 'bullet' }], // 리스트
            [{ 'align': [] }],                    // 정렬
            ['clean']                             // 서식 지우기
        ]
    }
});

async function submitPost() {
    const category = document.getElementById('category').value;
    const title = document.getElementById('title').value;
    // ★ 에디터의 내용을 HTML 태그 형태로 가져옵니다.
    const content = quill.root.innerHTML; 
    // 텍스트만 있는지 확인 (내용 없는 경우 체크)
    const textContent = quill.getText().trim();

    const token = localStorage.getItem('accessToken');

    if (!title || textContent.length === 0) {
        alert("제목과 내용을 모두 입력해주세요.");
        return;
    }

    try {
        const response = await fetch('/ecnm/info/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            // HTML 문자열 그대로 서버에 전송
            body: JSON.stringify({ category: category, 
                                   title: title, 
                                   content: content })
        });
        if (response.ok) {
            alert("게시글이 등록되었습니다!");
            window.location.href = 'info';
        } else {
            alert("등록 실패: 로그인 상태를 확인해주세요.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("서버 통신 오류");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // write.js에서 quill 객체를 전역으로 선언했다고 가정하거나, 여기서 접근 가능해야 함
    // 만약 write.js 내부 변수라면, write.js 안에 초기화 로직을 넣어야 합니다.
    
    const initialContent = document.getElementById('initial-content').innerHTML;
    // 내용이 있고, quill 객체가 존재한다면 내용 삽입
    if (initialContent.trim() !== "" && typeof quill !== 'undefined') {
        quill.root.innerHTML = initialContent;
    }
});

    // [수정 요청 함수]
async function updatePost() {
    const id = document.getElementById('postId').value;
    const title = document.getElementById('title').value;
    const category = document.getElementById('category').value;
    const content = quill.root.innerHTML; // Quill 에디터 내용 가져오기

    if (!title.trim()) { alert("제목을 입력하세요."); return; }

    try {
        const response = await fetch(`/ecnm/info/update/${id}`, {
            method: 'PUT', // 또는 POST (백엔드 설정에 따름)
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, category, content })
        });

        if (response.ok) {
            alert("수정이 완료되었습니다.");
            window.location.href = `/ecnm/info/post/${id}`; // 상세 페이지로 이동
        } else {
            alert("수정 실패: " + response.statusText);
        }
    } catch (error) {
        console.error(error);
        alert("오류가 발생했습니다.");
    }
}