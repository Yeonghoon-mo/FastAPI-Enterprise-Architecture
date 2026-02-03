# 🚀 FastAPI Layered Architecture Boilerplate

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-10.6%2B-003545?style=for-the-badge&logo=mariadb&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

> **Spring Boot 개발자를 위한 Python FastAPI 적응 가이드 프로젝트**  
> "Spring의 견고한 **3-Tier Architecture**를 FastAPI의 **가벼움**과 결합하다."

---

## 🏗 System Architecture

이 프로젝트는 유지보수성과 확장성을 고려하여 **관심사의 분리(Separation of Concerns)** 원칙을 철저히 준수합니다.

```mermaid
graph LR
    Client(Client) --> |Request| Router(Router/Controller)
    Router --> |DTO| Service(Service Layer)
    Service --> |Domain Model| Repository(Data Access Layer)
    Repository --> |SQL| DB[(MariaDB)]
```

### 📂 Directory Structure
Spring Boot의 패키지 구조와 1:1 매핑되도록 설계되었습니다.

```text
app/
├── core/               # [Global] 설정 및 공통 유틸리티
│   ├── config.py       # 환경변수 관리 (Pydantic Settings)
│   ├── database.py     # DB Connection Pool (SQLAlchemy Engine)
│   ├── security.py     # JWT 생성 및 비밀번호 Hashing (Bcrypt)
│   ├── logger.py       # Loguru 통합 로깅 시스템
│   └── dependencies.py # [AOP/Filter] 의존성 주입 (Token 검증 등)
│
├── models/             # [Entity] DB 테이블 스키마 정의
├── schemas/            # [DTO] 데이터 검증 및 API 입출력 모델
├── repository/         # [Repository] DB 접근 로직 (CRUD)
├── services/           # [Service] 비즈니스 로직 및 트랜잭션 단위
├── routers/            # [Controller] URL 라우팅 및 요청 처리
└── main.py             # [Application] 앱 진입점
```

---

## ✨ Key Features

### 🔐 1. Authentication & Security
- **JWT (JSON Web Token)** 기반 인증 시스템 구축.
- **BCrypt** 알고리즘을 사용한 비밀번호 단방향 암호화.
- **OAuth2PasswordBearer**를 통한 표준 보안 스키마 적용.
- `Depends(get_current_user)`를 통한 엔드포인트별 권한 제어 (Guard).

### 🛠 2. Robust CRUD Operations
- **Clean Code**: Router → Service → Repository 흐름의 명확한 역할 분리.
- **Data Validation**: Pydantic V2를 활용한 강력한 요청 데이터 검증.
- **Error Handling**: 명시적인 HTTP Exception 처리.
- **Cascade Delete**: SQLAlchemy `cascade` 설정을 통한 연관 데이터(댓글) 자동 삭제 관리.
- **Pagination**: Spring의 `Page` 객체를 벤치마킹한 공통 페이징 응답 구조 구축.

### ⚙️ 3. Configuration Management
- **Environment Variables**: `.env` 파일을 통한 민감 정보(DB, Secret Key) 분리.
- **Pydantic Settings**: 환경변수 타입 강제 및 유효성 검사.

### 📝 4. Advanced Logging
- **Loguru** 라이브러리 도입.
- Uvicorn의 시스템 로그를 가로채어(Intercept) 통일된 컬러 포맷으로 출력.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MariaDB (or MySQL)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yeonghoon-mo/fastapi-mariadb-crud.git
   cd fastapi-mariadb-crud
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   # .venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup (.env)**
   프로젝트 루트에 `.env` 파일을 생성하세요.
   ```ini
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=fastapi_db
   SECRET_KEY=your_secret_key_openssl_rand_hex_32
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run Server**
   ```bash
   # 개발 모드 (Auto Reload)
   uvicorn app.main:app --reload
   ```

### DB Migration (Alembic)

DB 스키마 변경 사항을 관리하기 위해 **Alembic**을 사용합니다.

- **마이그레이션 파일 생성** (모델 변경 후 실행)
  ```bash
  alembic revision --autogenerate -m "메시지"
  ```

- **DB 반영** (최신 버전으로 업데이트)
  ```bash
  alembic upgrade head
  ```

---

## 🗺️ Roadmap & Future Plans

이 프로젝트는 단순한 CRUD를 넘어, **엔터프라이즈급 백엔드 서버**로 발전하는 것을 목표로 합니다.

### Phase 1: Foundation (✅ Completed)
- [x] 프로젝트 구조 설계 (Layered Architecture)
- [x] MariaDB 연동 및 SQLAlchemy 설정
- [x] User CRUD (회원가입, 조회, 수정, 삭제)
- [x] JWT 로그인 및 보안 미들웨어 적용
- [x] 환경변수 관리 및 로깅 시스템 구축

### Phase 2: Domain Expansion (🚧 In Progress)
- [x] **Board Domain**: 게시글(Board) CRUD 기능 구현
- [x] **Relationships**: User(1) : Board(N) 일대다 관계 매핑 및 데이터 무결성 보장
- [x] **Board Domain**: 댓글(Comment) 기능 구현
- [x] **Relationships**: Board(1) : Comment(N) 및 User(1) : Comment(N) 관계 매핑
- [x] **Pagination**: 대용량 데이터를 위한 페이징 처리 (PageResponse 구현)
- [x] **File Upload**: 프로필 이미지 및 첨부파일 처리

### Phase 3: Advanced Tech
- [x] **Async I/O**: `async/await` 및 `aiomysql` 도입으로 완전 비동기 전환
- [ ] **Caching**: Redis를 활용한 데이터 캐싱 및 세션 관리
- [ ] **Background Tasks**: Celery 또는 RabbitMQ를 이용한 비동기 작업 처리 (이메일 발송 등)

### Phase 4: DevOps & Quality
- [ ] **Testing**: Pytest를 이용한 단위 테스트 및 통합 테스트 작성
- [ ] **Docker**: Dockerfile 및 docker-compose 구성
- [ ] **CI/CD**: GitHub Actions를 통한 자동 배포 파이프라인 구축

---

## 💡 Spring Boot vs FastAPI Comparison

| Feature | Spring Boot (Java) | FastAPI (Python) |
| :--- | :--- | :--- |
| **API Framework** | Spring MVC | FastAPI |
| **ORM** | JPA (Hibernate) | SQLAlchemy |
| **DTO** | Lombok `@Data` | Pydantic `BaseModel` |
| **Dependency Injection** | `@Autowired` / `@Bean` | `Depends()` |
| **Validation** | Bean Validation (`@NotNull`) | Pydantic Field Types |
| **Configuration** | `application.yml` | `pydantic-settings` |
| **Pagination** | `org.springframework.data.domain.Page` | `PageResponse` (Custom) |
| **Entry Point** | `public static void main` | `if __name__ == "__main__":` |

---

## 🛠 Technical Deep Dive (Portfolio)

### 1. File Upload Strategy
이미지 및 파일 업로드를 안전하고 효율적으로 처리하기 위해 다음과 같은 전략을 사용했습니다.

- **UUID Filename**: 사용자가 업로드한 파일명 중복을 방지하고 보안(경로 탐색 공격 방지)을 위해 `UUID v4`를 사용하여 파일명을 난수화했습니다.
- **Directory Isolation**: `static/uploads/profiles`와 `static/uploads/boards`로 디렉토리를 분리하여 관리 효율성을 높였습니다.
- **Service Layer Abstraction**: `FileService` 클래스를 별도로 구현하여 파일 저장/삭제 로직을 비즈니스 로직과 분리, 재사용성을 확보했습니다. (SRP 원칙)
- **Static Mounting**: FastAPI의 `StaticFiles`를 활용하여 별도의 웹 서버(Nginx 등) 없이도 개발 환경에서 즉시 이미지를 서빙할 수 있도록 구성했습니다.

### 2. DB Migration with Alembic
초기 개발 단계에서 잦은 DB 스키마 변경에 유연하게 대처하기 위해 **Alembic**을 도입했습니다.

- **Problem**: 모델(`models.py`) 수정 후 테이블을 수동으로 `DROP` & `CREATE` 하거나, 직접 `ALTER` 쿼리를 작성해야 하는 번거로움과 위험성 존재.
- **Solution**: Alembic을 통해 Python 모델 코드의 변경 사항을 감지하여 자동으로 마이그레이션 스크립트를 생성(`--autogenerate`)하고, 버전 관리(Versioning)가 가능하도록 구축했습니다.
- **Workflow**: `Model 수정` -> `alembic revision` -> `alembic upgrade`

---

## 👨‍💻 Maintainer

**Mo Yeonghoon**
- Backend Developer (Java/Kotlin, Python)
- Github: [@Yeonghoon-mo](https://github.com/Yeonghoon-mo)