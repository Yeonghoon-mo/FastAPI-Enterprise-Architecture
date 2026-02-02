from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_by_board(db: Session, board_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.board_id == board_id).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate, board_id: int, user_id: str):
    db_comment = Comment(**comment.model_dump(), board_id=board_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, db_comment: Comment, comment_update: CommentUpdate):
    update_data = comment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()
