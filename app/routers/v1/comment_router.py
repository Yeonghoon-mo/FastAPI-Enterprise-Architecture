from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services import comment_service
from app.models.user import User
from app.core.rate_limiter import RateLimiter

router = APIRouter(
    tags=["comments"],
)

# 댓글 작성
@router.post(
    "/boards/{board_id}/comments", 
    response_model=CommentResponse, 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="댓글 작성",
    description="특정 게시글에 새로운 댓글을 작성합니다. **1분에 10회**로 요청이 제한됩니다.",
    responses={
        201: {"description": "댓글 작성 성공"},
        401: {"description": "인증 실패 (토큰 누락)"},
        404: {"description": "게시글을 찾을 수 없음"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def create_comment(
    board_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.create_new_comment(
        db=db, comment=comment, board_id=board_id, user_id=current_user.email
    )

# 특정 게시글의 댓글 목록 조회
@router.get(
    "/boards/{board_id}/comments", 
    response_model=List[CommentResponse],
    summary="특정 게시글의 댓글 목록 조회",
    description="게시글 ID를 기반으로 해당 게시글에 달린 모든 댓글 목록을 조회합니다.",
    responses={
        200: {"description": "댓글 목록 조회 성공"},
        404: {"description": "게시글을 찾을 수 없음"}
    }
)
async def read_comments(
    board_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await comment_service.get_comments_for_board(
        db=db, board_id=board_id, skip=skip, limit=limit
    )

# 댓글 수정
@router.put(
    "/comments/{comment_id}", 
    response_model=CommentResponse, 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="댓글 수정",
    description="기존 댓글 내용을 수정합니다. 본인이 작성한 댓글만 수정 가능합니다.",
    responses={
        200: {"description": "수정 성공"},
        403: {"description": "권한 부족 (본인 아님)"},
        404: {"description": "댓글을 찾을 수 없음"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.update_existing_comment(
        db=db, comment_id=comment_id, comment_update=comment_update, user_id=current_user.email
    )

# 댓글 삭제
@router.delete(
    "/comments/{comment_id}", 
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="댓글 삭제",
    description="기존 댓글을 영구적으로 삭제합니다. 본인이 작성한 댓글만 삭제 가능합니다.",
    responses={
        200: {"description": "삭제 성공"},
        403: {"description": "권한 부족 (본인 아님)"},
        404: {"description": "댓글을 찾을 수 없음"},
        429: {"description": "요청 횟수 초과"}
    }
)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await comment_service.delete_existing_comment(
        db=db, comment_id=comment_id, user_id=current_user.email
    )