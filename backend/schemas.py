from pydantic import BaseModel
from datetime import datetime  # ★ 날짜 처리를 위해 추가 필요
from typing import List, Optional

# --- [기존 회원 관련 스키마 (그대로 유지)] ---
class UserCreate(BaseModel):
    username: str
    password: str
    email: str      # 추가
    nickname: str   # 추가
    phone: str      # 추가

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str      # 응답에도 포함하고 싶다면 추가
    nickname: str   # 응답에도 포함하고 싶다면 추가
    class Config:
        from_attributes = True 

# --- [▼ 여기에 게시판 스키마 추가] ---

# 1. 글 작성할 때 (클라이언트 -> 서버)
# 제목과 내용만 받습니다. (작성자 ID는 서버에서 처리)
class PostCreate(BaseModel):
    title: str
    content: str

# 2. 글 조회할 때 (서버 -> 클라이언트)
# DB에 저장된 ID, 작성일, 작성자ID(owner_id)를 포함해서 돌려줍니다.
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime | None = None # 작성일
    owner_id: int        # 작성자 ID (누가 썼는지 식별)

    class Config:
        from_attributes = True # ORM 객체 매핑 허용