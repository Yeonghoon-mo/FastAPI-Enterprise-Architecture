from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

# [Spring: @Repository]
# DB 접근 로직을 담당하는 계층입니다. (Data Access Layer)

# [Java: Optional<User> findById(Long id)]
# ID로 사용자를 조회합니다.
def get_user(db: Session, user_id: int):
    # db.query(User) == SELECT * FROM users
    # .filter(User.id == user_id) == WHERE id = ?
    # .first() == limit 1 (없으면 None 반환)
    return db.query(User).filter(User.id == user_id).first()

# [Java: Optional<User> findByEmail(String email)]
# 이메일로 사용자를 조회합니다. (중복 가입 체크용)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# [Java: User save(User user)]
# 사용자를 생성하고 저장합니다.
def create_user(db: Session, user: UserCreate):
    # TODO: 실제로는 BCryptPasswordEncoder 등을 사용해 비밀번호를 암호화해야 합니다.
    fake_hashed_password = user.password + "notreallyhashed"
    
    # Entity 생성 (Builder 패턴 대신 생성자 사용)
    db_user = User(email=user.email, hashed_password=fake_hashed_password)

    # 1. 영속성 컨텍스트(Persistence Context)에 추가 (Staging)
    db.add(db_user)
    
    # 2. 트랜잭션 커밋 (DB에 SQL 전송)
    db.commit()
    
    # 3. DB에서 생성된 데이터(Auto Increment ID 등)를 다시 가져옴
    db.refresh(db_user)
    
    return db_user