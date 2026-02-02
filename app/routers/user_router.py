from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, User
from app.repository import user_repository

# [Spring: @RestController + @RequestMapping("/users")]
# API 엔드포인트를 정의하는 컨트롤러입니다.
router = APIRouter(
    prefix="/users",
    tags=["users"],  # Swagger UI에서 'users' 그룹으로 묶여서 보입니다.
)

# [Spring: @PostMapping("/")]
# response_model=User: 반환 타입을 User DTO로 지정 (자동 변환)
@router.post("/", response_model=User)
def create_user(
    user: UserCreate, # [Spring: @RequestBody]
    db: Session = Depends(get_db) # [Spring: @Autowired / 의존성 주입]
):
    # 중복 이메일 체크
    db_user = user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        # [Spring: throw new ResponseStatusException(HttpStatus.BAD_REQUEST, ...)]
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_repository.create_user(db=db, user=user)

# [Spring: @GetMapping("/{userId}")]
@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int, # [Spring: @PathVariable]
    db: Session = Depends(get_db)
):
    db_user = user_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user