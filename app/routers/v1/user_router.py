from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, RoleChecker
from app.schemas.user import UserCreate, User, UserUpdate
from app.services import user_service
from app.services.file_service import FileService
from app.models.user import User as UserModel, UserRole  # 타입 힌트 및 역할 Enum

# [Spring: @RestController]
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 권한 가드 정의
admin_only = RoleChecker([UserRole.ADMIN])

# 모든 유저 조회 (관리자 전용)
@router.get(
    "/", 
    response_model=list[User], 
    dependencies=[Depends(admin_only)],
    summary="전체 사용자 목록 조회",
    description="시스템에 등록된 모든 사용자의 정보를 조회합니다. **관리자 권한**이 필요합니다.",
    responses={
        403: {"description": "권한 부족 (관리자만 접근 가능)"},
        401: {"description": "인증 실패 (유효하지 않은 토큰)"}
    }
)
async def read_all_users(db: AsyncSession = Depends(get_db)):
    return await user_service.get_users(db=db)

# 프로필 이미지 업로드 (로그인 필수 + 본인만 가능)
@router.post(
    "/{email}/profile-image", 
    response_model=User,
    summary="프로필 이미지 업로드",
    description="사용자의 프로필 이미지를 업로드하고 URL을 업데이트합니다. 본인 계정에 대해서만 작업이 가능합니다.",
    responses={
        200: {"description": "이미지 업로드 및 정보 업데이트 성공"},
        403: {"description": "인증 실패 (본인 아님)"},
        413: {"description": "파일 크기 초과"},
        429: {"description": "요청 횟수 초과 (Rate Limit)"}
    }
)
async def upload_profile_image(
    email: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 본인 확인
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
    
    # 1. 기존 이미지가 있다면 삭제
    if current_user.profile_image_url:
        FileService.delete_file(current_user.profile_image_url)
    
    # 2. 새 이미지 저장
    image_url = await FileService.save_file(file, sub_dir="profiles")
    
    # 3. DB 업데이트
    return await user_service.update_profile_image(db=db, email=email, image_url=image_url)

# 회원가입 (누구나 가능)
@router.post(
    "/", 
    response_model=User,
    summary="신규 회원 가입",
    description="새로운 사용자를 등록합니다. 이메일 중복 체크가 포함되어 있습니다.",
    responses={
        201: {"description": "회원 가입 성공"},
        400: {"description": "이미 존재하는 이메일"},
        422: {"description": "데이터 유효성 검사 실패"}
    }
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db=db, user=user)

# 회원 조회 (누구나 가능)
@router.get(
    "/{email}", 
    response_model=User,
    summary="특정 사용자 정보 조회",
    description="이메일을 기반으로 사용자의 상세 정보를 조회합니다.",
    responses={
        200: {"description": "조회 성공"},
        404: {"description": "사용자를 찾을 수 없음"}
    }
)
async def read_user(email: str, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user(db=db, email=email)

# 회원 수정 (로그인 필수 + 본인만 가능)
@router.put(
    "/{email}", 
    response_model=User,
    summary="사용자 정보 수정",
    description="사용자의 비밀번호, 활성 상태 등을 수정합니다. 본인 계정에 대해서만 수정이 가능합니다.",
    responses={
        200: {"description": "수정 성공"},
        403: {"description": "인증 실패 (본인 아님)"},
        404: {"description": "사용자를 찾을 수 없음"},
        429: {"description": "요청 횟수 초과 (Rate Limit)"}
    }
)
async def update_user(
    email: str, 
    user_update: UserUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 본인 확인
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return await user_service.update_user(db=db, email=email, user_update=user_update)

# 회원 삭제 (로그인 필수 + 본인만 가능)
@router.delete(
    "/{email}",
    summary="사용자 계정 삭제",
    description="사용자 계정을 영구적으로 삭제합니다. 본인 계정에 대해서만 삭제가 가능합니다.",
    responses={
        200: {"description": "삭제 성공"},
        403: {"description": "인증 실패 (본인 아님)"},
        404: {"description": "사용자를 찾을 수 없음"},
        429: {"description": "요청 횟수 초과 (Rate Limit)"}
    }
)
async def delete_user(
    email: str, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 본인 확인
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="인증 실패")
        
    return await user_service.delete_user(db=db, email=email)