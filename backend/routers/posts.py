# backend/routers/posts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database, schemas, crud, models, auth

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# 1. 게시글 목록 조회 (누구나 볼 수 있음)
# 주소: GET /posts/
@router.get("/", response_model=List[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

# 2. 게시글 작성 (★로그인한 사람만 가능★)
# 주소: POST /posts/
@router.post("/", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user) # 여기서 토큰 검사!
):
    return crud.create_post(db=db, post=post, user_id=current_user.id)