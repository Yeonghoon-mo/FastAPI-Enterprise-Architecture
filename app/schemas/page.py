from pydantic import BaseModel, ConfigDict
from typing import TypeVar, Generic, List

T = TypeVar("T")

# [Spring: Page<T> 인터페이스 느낌!]
class PageResponse(BaseModel, Generic[T]):
    items: List[T]          # 데이터 목록 (content)
    total_count: int       # 전체 아이템 수 (totalElements)
    page: int              # 현재 페이지 (number)
    size: int              # 페이지 당 아이템 수 (size)
    total_pages: int       # 전체 페이지 수 (totalPages)

    model_config = ConfigDict(from_attributes=True)
