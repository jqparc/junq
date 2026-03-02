from fastapi import APIRouter
from .ecnm import router as ecnm_router
from .idct.idct import router as idct_router
from .info.info import router as info_router
# 나중에 추가될 기능들:
# from .news.news import router as news_router 

# ecnm 관련 기능을 모두 담는 통합 라우터 생성
# ecnm_router = APIRouter(prefix="/ecnm", tags=["ecnm"])

# 하위 라우터들을 포함시킴
ecnm_router.include_router(idct_router)
ecnm_router.include_router(info_router)
# ecnm_router.include_router(news_router)