from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse
from app.schemas.page import PageResponse
from app.services import board_service
from app.services.file_service import FileService
from app.models.user import User
from app.core.rate_limiter import RateLimiter

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)

# 글쓰기 (Multipart/form-data)
@router.post(
    "/", 
    response_model=BoardResponse, 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="게시글 작성",
    description="새로운 게시글을 작성합니다. 이미지 파일을 첨부할 수 있으며, **Multipart/form-data** 형식을 사용합니다. 1분에 5회 제한됩니다.",
    responses={
        201: {"description": "게시글 작성 성공"},
        401: {"description": "인증 실패 (토큰 누락)"},
        429: {"description": "도배 방지 (요청 횟수 초과)"}
    }
)
async def create_board(
    title: str = Form(..., description="게시글 제목"),
    content: str = Form(..., description="게시글 본문"),
    file: Optional[UploadFile] = File(None, description="첨부 이미지 파일"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if file:
        image_url = await FileService.save_file(file, sub_dir="boards")
        
    board = BoardCreate(title=title, content=content)
    return await board_service.create_new_board(db=db, board=board, user_id=current_user.email, image_url=image_url)

# 수정 (Multipart/form-data)
@router.put(
    "/{board_id}", 
    response_model=BoardResponse, 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="게시글 수정",
    description="기존 게시글을 수정합니다. 본인 게시글만 수정 가능하며, 새 이미지를 업로드하면 기존 이미지는 대체됩니다.",
    responses={
        200: {"description": "수정 성공"},
        403: {"description": "권한 부족 (본인 아님)"},
        404: {"description": "게시글을 찾을 수 없음"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def update_board(
    board_id: int,
    title: Optional[str] = Form(None, description="수정할 제목"),
    content: Optional[str] = Form(None, description="수정할 본문"),
    file: Optional[UploadFile] = File(None, description="새 첨부 이미지 파일"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if file:
        image_url = await FileService.save_file(file, sub_dir="boards")
    
    board_update = BoardUpdate(title=title, content=content)
    return await board_service.update_existing_board(
        db=db, board_id=board_id, board_update=board_update, user_id=current_user.email, image_url=image_url
    )

# 목록 조회 (Pagination 적용)
@router.get(
    "/", 
    response_model=PageResponse[BoardResponse],
    summary="게시글 목록 조회 (페이징)",
    description="전체 게시글 목록을 최신순으로 페이징하여 조회합니다.",
    responses={
        200: {"description": "목록 조회 성공"}
    }
)
async def read_boards(
    page: int = 1, 
    size: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    return await board_service.get_boards_list(db=db, page=page, size=size)

# 단건 조회
@router.get(
    "/{board_id}", 
    response_model=BoardResponse,
    summary="게시글 상세 조회",
    description="특정 ID를 가진 게시글의 상세 정보를 조회합니다.",
    responses={
        200: {"description": "조회 성공"},
        404: {"description": "게시글을 찾을 수 없음"}
    }
)
async def read_board(board_id: int, db: AsyncSession = Depends(get_db)):
    return await board_service.get_board_detail(db=db, board_id=board_id)

# 삭제
@router.delete(
    "/{board_id}", 
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    summary="게시글 삭제",
    description="기존 게시글을 영구적으로 삭제합니다. 본인 게시글만 삭제 가능합니다.",
    responses={
        200: {"description": "삭제 성공"},
        403: {"description": "권한 부족 (본인 아님)"},
        404: {"description": "게시글을 찾을 수 없음"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def delete_board(
    board_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await board_service.delete_existing_board(db=db, board_id=board_id, user_id=current_user.email)