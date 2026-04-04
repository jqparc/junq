from fastapi import APIRouter, Depends, HTTPException
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
import database, schemas, models, crud, auth

nav_dtl_tab = [ 
    {"id": "idct", "name": "시장지표", "url": "/ecnm/idct"},
    {"id": "info", "name": "인사이트", "url": "/ecnm/info"} 
] 

router = APIRouter(prefix="/info", tags=["info"])

# 2. 템플릿(HTML) 폴더 위치 찾기
# (현재 파일 위치에서 두 단계 위로 올라가서 templates 폴더 찾음)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/write", name="ecnm.info.write")
def ecnm_write(request: Request):
    # home.html을 브라우저에 보여줍니다.
    return templates.TemplateResponse("ecnm/info/post_write.html", {
        "request": request, 
        "active_top": "ecnm",  
        "active_dtl": "info", 
        "nav_dtl_tabs": nav_dtl_tab
    })

@router.get("/posts", response_model=List[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

# 2. 게시글 작성 (로그인 필요)
@router.post("/posts", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int):
    return templates.TemplateResponse("ecnm/info/post_read.html", {
        "request": request, 
        "post_id": post_id,
        "active_top": "ecnm",  
        "active_dtl": "info", 
        "nav_dtl_tabs": nav_dtl_tab
    })

# 상세 페이지 데이터 반환 (JSON)
@router.get("/read/{post_id}", response_model=schemas.PostResponse)
def read_post_data(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/update/{post_id}")
def update_post_page(request: Request, post_id: int, db: Session = Depends(database.get_db)):
    # DB에서 게시글 가져오기
    post = crud.get_post(db, post_id) 
    
    return templates.TemplateResponse("ecnm/info/post_write.html", {
        "request": request, 
        "post": post,
        "active_top": "ecnm",  
        "active_dtl": "info", 
        "nav_dtl_tabs": nav_dtl_tab
    })

@router.put("/update/{post_id}", response_model=schemas.PostResponse)
def update_post_api(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db=db, post_id=post_id, post=post)
    
    if not updated_post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        
    return updated_post

@router.delete("/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # 1) 먼저 DB에서 해당 게시글이 있는지 찾습니다.
    post = crud.get_post(db, post_id=post_id)
    
    # 2) 글이 없으면 에러 반환
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    # 3) 글이 있으면 삭제 후 반영
    db.delete(post)
    db.commit()
    
    return {"message": "게시글이 성공적으로 삭제되었습니다."}