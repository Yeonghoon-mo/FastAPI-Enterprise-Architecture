from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository import board_repository
from app.schemas.board import BoardCreate, BoardUpdate
from app.services.file_service import FileService

import math
from app.schemas.page import PageResponse

def create_new_board(db: Session, board: BoardCreate, user_id: str, image_url: str = None):
    return board_repository.create_board(db=db, board=board, user_id=user_id, image_url=image_url)

def get_boards_list(db: Session, page: int = 1, size: int = 10):
    skip = (page - 1) * size
    items = board_repository.get_boards(db=db, skip=skip, limit=size)
    total_count = board_repository.get_boards_count(db=db)
    total_pages = math.ceil(total_count / size) if total_count > 0 else 0
    
    return PageResponse(
        items=items,
        total_count=total_count,
        page=page,
        size=size,
        total_pages=total_pages
    )

def get_board_detail(db: Session, board_id: int):
    db_board = board_repository.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

def update_existing_board(db: Session, board_id: int, board_update: BoardUpdate, user_id: str, image_url: str = None):
    db_board = get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this board")
    
    # 이미지 업데이트 시 기존 이미지 삭제
    if image_url:
        if db_board.image_url:
            FileService.delete_file(db_board.image_url)
        db_board.image_url = image_url
        
    return board_repository.update_board(db=db, db_board=db_board, board_update=board_update)

def delete_existing_board(db: Session, board_id: int, user_id: str):
    db_board = get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
    
    # 게시글 삭제 시 첨부 이미지도 삭제
    if db_board.image_url:
        FileService.delete_file(db_board.image_url)
        
    board_repository.delete_board(db=db, db_board=db_board)
    return {"message": "Board deleted successfully"}