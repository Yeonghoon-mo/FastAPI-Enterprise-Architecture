from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse
from app.schemas.page import PageResponse
from app.services import board_service
from app.models.user import User

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
)

# 글쓰기
@router.post("/", response_model=BoardResponse)
def create_board(
    board: BoardCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return board_service.create_new_board(db=db, board=board, user_id=current_user.email)

# 목록 조회 (Pagination 적용)
@router.get("/", response_model=PageResponse[BoardResponse])
def read_boards(
    page: int = 1, 
    size: int = 10, 
    db: Session = Depends(get_db)
):
    return board_service.get_boards_list(db=db, page=page, size=size)

# 단건 조회
@router.get("/{board_id}", response_model=BoardResponse)
def read_board(board_id: int, db: Session = Depends(get_db)):
    return board_service.get_board_detail(db=db, board_id=board_id)

# 수정
@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int, 
    board_update: BoardUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return board_service.update_existing_board(
        db=db, board_id=board_id, board_update=board_update, user_id=current_user.email
    )

# 삭제
@router.delete("/{board_id}")
def delete_board(
    board_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return board_service.delete_existing_board(db=db, board_id=board_id, user_id=current_user.email)