from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# 1. 회원 테이블 (게시글의 주인)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    nickname = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    address = Column(String)
    
    # 이 유저가 쓴 글 목록 (Post 테이블과 연결)
    posts = relationship("Post", back_populates="owner")

# 2. 게시글 테이블
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)      # 제목
    content = Column(Text)                  # 내용
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 작성시간
    
    # ★ 외래키: users 테이블의 id를 참조합니다.
    owner_id = Column(Integer, ForeignKey("users.id"))

    # 작성자 정보 (User 테이블과 연결)
    owner = relationship("User", back_populates="posts")