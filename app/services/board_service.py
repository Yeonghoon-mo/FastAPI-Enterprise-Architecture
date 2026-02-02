from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository import board_repository
from app.schemas.board import BoardCreate, BoardUpdate

def create_new_board(db: Session, board: BoardCreate, user_id: str):
    return board_repository.create_board(db=db, board=board, user_id=user_id)

def get_boards_list(db: Session, skip: int = 0, limit: int = 100):
    return board_repository.get_boards(db=db, skip=skip, limit=limit)

def get_board_detail(db: Session, board_id: int):
    db_board = board_repository.get_board(db, board_id=board_id)
    if db_board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board

def update_existing_board(db: Session, board_id: int, board_update: BoardUpdate, user_id: str):
    db_board = get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this board")
        
    return board_repository.update_board(db=db, db_board=db_board, board_update=board_update)

def delete_existing_board(db: Session, board_id: int, user_id: str):
    db_board = get_board_detail(db, board_id)
    
    # 본인 확인
    if db_board.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this board")
        
    board_repository.delete_board(db=db, db_board=db_board)
    return {"message": "Board deleted successfully"}