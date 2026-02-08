from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas, crud, models
from database import get_db
from fastapi import Request
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates  # 임포트 확인
# 위에서 만든 dependencies를 가져옵니다
from auth import get_current_user 

# URL 앞에 자동으로 /ecnm_info 가 붙도록 설정
router = APIRouter(
    prefix="/ecnm_info",
    tags=["ecnm_info"]
)

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 1. 게시글 목록 조회
# 실제 주소: GET /ecnm_info/posts
@router.get("/posts", response_model=List[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

# 2. 게시글 작성 (로그인 필요)
# 실제 주소: POST /ecnm_info/posts
@router.post("/posts", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int):
    return templates.TemplateResponse("ecnm/ecnm_info/post_detail.html", {"request": request, "post_id": post_id})

# 상세 페이지 데이터 반환 (JSON)
@router.get("/read/{post_id}", response_model=schemas.PostResponse)
def read_post_data(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post