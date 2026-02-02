from sqlalchemy.orm import Session
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate

def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()

def get_boards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Board).order_by(Board.id.desc()).offset(skip).limit(limit).all()

def get_boards_count(db: Session):
    return db.query(Board).count()

def create_board(db: Session, board: BoardCreate, user_id: str):
    db_board = Board(**board.model_dump(), user_id=user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def update_board(db: Session, db_board: Board, board_update: BoardUpdate):
    update_data = board_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_board, key, value)
    
    db.commit()
    db.refresh(db_board)
    return db_board

def delete_board(db: Session, db_board: Board):
    db.delete(db_board)
    db.commit()