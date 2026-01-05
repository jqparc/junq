from sqlalchemy.orm import Session
import models, schemas, auth

# --- [기존 코드: 회원 관련] (그대로 두세요) ---

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    # models.User에 정의된 필드명에 맞춰 저장
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- [▼ 추가 코드: 게시판 관련] ---

# 1. 게시글 목록 조회 (최신순 정렬)
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).order_by(models.Post.id.desc()).offset(skip).limit(limit).all()

# 2. 게시글 작성
def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    # 스키마(title, content) + 유저ID(owner_id)를 합쳐서 DB 모델 생성
    db_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=user_id 
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post