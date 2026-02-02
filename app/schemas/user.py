from pydantic import BaseModel, ConfigDict

# [DTO: Data Transfer Object]
# Spring의 DTO와 같습니다. Lombok의 @Data가 기본 적용된 것과 비슷합니다.

# 1. 공통 속성 (Base DTO)
class UserBase(BaseModel):
    # [Validation: @NotNull] (타입이 Optional이 아니면 필수값)
    email: str

# 2. 생성 요청 DTO (Request Body)
# 회원가입 시 클라이언트가 보내주는 데이터 구조입니다.
class UserCreate(UserBase):
    # 비밀번호는 생성할 때만 필요하고, 응답으로 줄 땐 빼야 하므로 여기에만 정의합니다.
    password: str

# 3. 응답 DTO (Response Body)
# 클라이언트에게 돌려줄 데이터 구조입니다. (비밀번호 제외, ID 포함)
class User(UserBase):
    id: int
    is_active: bool

    # [ModelMapper / MapStruct 역할]
    # JPA Entity(ORM 객체)를 Pydantic DTO로 자동으로 변환해주는 설정입니다.
    # user_entity.id -> user_dto.id 매핑을 알아서 해줍니다.
    model_config = ConfigDict(from_attributes=True)
