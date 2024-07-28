# from datetime import datetime, timedelta, timezone
# from typing import Annotated

# import jwt  # JWT 토큰을 생성하고 검증하기 위해 사용
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # OAuth2를 사용한 인증
# from jwt.exceptions import InvalidTokenError  # JWT 토큰 예외 처리
# from passlib.context import CryptContext  # 비밀번호 해싱을 위해 사용
# from pydantic import BaseModel, EmailStr  # 데이터 검증을 위한 Pydantic 모델
# from fastapi import Form


# ####################################################################################################
# """
# model
# """
# # 가상의 사용자 데이터베이스 (선생님)
# fake_teacher_db = {
#     "jane@example.com": {
#         "full_name": "Jane Smith",
#         "email": "jane@example.com",
#         "hashed_password": "$2b$12$XyzZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#         "scope": "teacher",
#     }
# }

# # 가상의 사용자 데이터베이스 (학생)
# fake_student_db = {
#     "johndoe@example.com": {
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#         "scope": "student",
#     }
# }


# # 사용자 정보를 저장하는 모델 정의
# class User(BaseModel):
#     full_name: str
#     email: str
#     disabled: bool
#     scope: str
    
# ####################################################################################################
# """
# security
# """
# # 비밀 키와 알고리즘 설정
# # SECRET_KEY는 JWT 토큰을 서명하기 위해 사용되는 비밀 키
# # ALGORITHM은 토큰 서명에 사용될 알고리즘을 지정
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 액세스 토큰의 만료 시간(분 단위)
# STUDENT_SCOPE = "student"
# TEACHER_SCOPE = "teacher"


# class Crypto:
#     '''
#     비밀번호 해싱 및 검증을 위한 클래스
#     '''
#     # 비밀번호 해싱 및 검증을 위한 PassLib 컨텍스트 생성
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    
#     @classmethod
#     def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
#         '''
#         - 평문 비밀번호와 해싱된 비밀번호를 비교하는 함수
#         - 사용자가 입력한 비밀번호와 저장된 해시된 비밀번호를 비교
#         '''
#         return cls.pwd_context.verify(plain_password, hashed_password)

#     @classmethod
#     def get_password_hash(cls, password: str) -> str:
#         '''
#         - 비밀번호를 해싱하는 함수
#         - 새로운 사용자 생성 시 비밀번호를 해싱하여 저장
#         '''
#         return cls.pwd_context.hash(password)

    
# class JWT:
#     @staticmethod
#     def create_access_token(data: dict, expires_delta: timedelta | None = None):
#         '''
#         - JWT 액세스 토큰을 생성하는 함수
#         - 사용자 정보를 포함한 JWT 토큰을 생성하고 반환
#         '''
#         to_encode = data.copy()
#         if expires_delta:
#             expire = datetime.now(timezone.utc) + expires_delta
#         else:
#             expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#         to_encode.update({"exp": expire})
#         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#         return encoded_jwt


#     @staticmethod
#     def decode_token(token: str) -> dict:
#         """
#         - JWT 토큰을 디코딩 하는 함수
#         - 주어진 JWT 토큰을 해독하여 포함된 내용을 반환
#         - 유효하지 않은 토큰인 경우 HTTP 예외처리
#         """
#         try:
#             return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         except InvalidTokenError:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Could not validate credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )



# # OAuth2PasswordBearer: "/token" 엔드포인트를 사용하여 토큰을 얻도록 설정
# # 클라이언트가 토큰을 얻기 위해 이 URL을 호출
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token", # "/api/auth",
#     scopes={"student": "Access as student", "teacher": "Access as teacher"}
# )


# ####################################################################################################
# """
# main
# """

# # FastAPI 애플리케이션 인스턴스 생성
# app = FastAPI()

# ####################################################################################################
# """ 
# Auth DTO
# """
# # 토큰 데이터 모델 정의
# # 클라이언트에게 반환되는 액세스 토큰과 토큰 유형을 포함
# class Token(BaseModel):
#     access_token: str
#     token_type: str


# # 데이터베이스에서 사용자 정보를 저장하는 모델 정의 (해싱된 비밀번호 포함)
# # User 모델을 확장하여 비밀번호 해시를 포함
# class UserInDB(User):
#     hashed_password: str


# # 토큰에서 사용자 이름을 저장하는 데이터 모델 정의
# # JWT에서 추출한 사용자 이름을 저장
# class TokenData(BaseModel):
#     email: str | None = None
#     scope: str | None = None


# """ 
# Auth DAO
# """
# # import logging
# # from sqlalchemy import select 
# # from sqlalchemy.ext.asyncio import AsyncSession

# # from src.database.model import UserTeacher, UserStudent

# # async def get_student_user(db: AsyncSession, username: str):
# #     student_result = await db.execute(select(UserStudent).filter(UserStudent.student_email == username).limit(1))
# #     student = student_result.scalars().first()
# #     if student:
# #         logging.info(f"Student info: {student.student_email, student.student_password}")
# #         return student.student_password, student.student_email
# #     else:
# #         return None, None

# # async def get_teacher_user(db: AsyncSession, username: str):
# #     teacher_result = await db.execute(select(UserTeacher).filter(UserTeacher.teacher_email == username).limit(1))
# #     teacher = teacher_result.scalars().first()
# #     if teacher:
# #         logging.info(f"Teacher info: {teacher.teacher_email, teacher.teacher_password}")
# #         return teacher.teacher_password, teacher.teacher_email
# #     else:
# #         return None, None

# def get_teacher_user(fake_teacher_db, email: str):
#     ''' 
#     - 데이터베이스에서 사용자 정보를 가져오는 함수
#     - 사용자 이름을 이용하여 데이터베이스에서 사용자 정보를 검색
#     '''
#     if email in fake_teacher_db:
#         user_dict = fake_teacher_db[email]
#         return UserInDB(**user_dict)


# def get_student_user(fake_student_db, email: str):
#     ''' 
#     - 데이터베이스에서 사용자 정보를 가져오는 함수
#     - 사용자 이름을 이용하여 데이터베이스에서 사용자 정보를 검색
#     '''
#     if email in fake_student_db:
#         user_dict = fake_student_db[email]
#         return UserInDB(**user_dict)
    

# """
# Auth Service
# """
# # async def authenticate_user(username: str, password: str, scope: str, db: AsyncSession):
# #     if scope == STUDENT_SCOPE:
# #         user = await login_dao.get_student_user(db, username)
# #     elif scope == TEACHER_SCOPE:
# #         user = await login_dao.get_teacher_user(db, username)
# #     else:
# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid scope"
# #         )

# #     if not user or not pwd_context.verify(password, user[0]):
# #         raise HTTPException(
# #             status_code=401,
# #             detail="Incorrect email or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
# #     logger.info(f"{scope.capitalize()} user authenticated: {username}")
# #     return user[1]


# # def authenticate_user(fake_db, email: str, password: str):
# #     '''
# #     - 사용자 인증 함수 (비밀번호 검증)
# #     - 사용자의 이름과 비밀번호를 검증하여 유효한 사용자인지 확인
# #     '''
# #     user = get_user(fake_db, email)
# #     if not user:
# #         return False
# #     if not Crypto.verify_password(password, user.hashed_password):
# #         return False
# #     return user


# async def authenticate_user(username: str, password: str, scope: str, db: AsyncSession):
#     '''
#     - 사용자 인증 함수 (비밀번호 검증)
#     - 사용자의 이름과 비밀번호를 검증하여 유효한 사용자인지 확인
#     '''
#     if scope == STUDENT_SCOPE:
#         user = await get_student_user(fake_student_db, username)
#     elif scope == TEACHER_SCOPE:
#         user = await get_teacher_user(fake_teacher_db, username)
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid scope"
#         )

#     if not user or not Crypto.verify_password(password, user.hashed_password):
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user



# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     ''' 
#     - 현재 사용자 정보를 가져오는 함수 (JWT 토큰에서 사용자 정보 추출)
#     - JWT 토큰을 디코딩하여 사용자 정보를 추출하고 검증
#     '''
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = JWT.decode_token(token)
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if email is None or role is None:
#             raise credentials_exception
#         token_data = TokenData(email=email, role=role)
#     except InvalidTokenError:
#         raise credentials_exception
#     db = fake_teacher_db if token_data.role == "teacher" else fake_student_db
#     user = get_user(db, token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user



# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     ''' 
#     - 활성 사용자만 가져오는 함수 (비활성화된 사용자 확인)
#     - 현재 사용자 정보에서 계정 비활성화 여부를 확인하고 활성 사용자만 반환    
#     '''
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



# """ 
# Auth - Control
# """
# @app.post(
#     "/login",
#     summary="액세스 토큰을 발급하는 로그인 엔드포인트",
#     description="- 사용자가 자격 증명(OAuth2PasswordRequestForm)을 제출하면 액세스 토큰을 발급",
#     response_model=Token
# )
# async def login_for_access_token(
#     form_data: LoginForm
# ) -> Token:
#     db = fake_teacher_db if form_data.email in fake_teacher_db else fake_student_db
#     user = authenticate_user(db, form_data.email, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",  # 메시지도 이메일로 수정
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = JWT.create_access_token(
#         data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")




# @app.get(
#     "/user/info", 
#     summary="현재 사용자 정보를 반환하는 엔드포인트",
#     description="- 인증된 사용자에 대한 정보를 반환",
#     response_model=User
# )
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user


# @app.get(
#     "/user/items",
#     summary="현재 사용자가 소유한 항목을 반환하는 엔드포인트",
#     description="- 사용자가 소유한 특정 아이템 목록을 반환",
# )
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.email}]


# ####################################################################################################
# '''
# User DTO
# '''
# # 회원가입을 위한 모델 정의
# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str
#     full_name: str
#     role: str
    
    
    
# """
# User Control + DAO + Service
# """
# @app.post(
#     "/signup",
#     summary="회원가입 엔드포인트",
#     description="- 데이터베이스에 새로운 사용자 추가"
# )
# async def register_user(user: UserCreate):
#     db = fake_teacher_db if user.role == "teacher" else fake_student_db
#     if user.email in db:
#         raise HTTPException(
#             status_code=400, detail="Email already registered"
#         )
#     user_dict = user.dict()
#     hashed_password = Crypto.get_password_hash(user.password)
#     user_dict['hashed_password'] = hashed_password
#     del user_dict['password']
#     db[user.email] = user_dict
#     return {"msg": "User registered successfully"}



# # Control 레이어
# @app.get("/user/data")
# async def user_data(current_user: Annotated[User, Depends(get_current_user)]):
#     if current_user.role == "teacher":
#         return await get_teacher_data(current_user)
#     elif current_user.role == "student":
#         return await get_student_data(current_user)
#     else:
#         raise HTTPException(status_code=403, detail="Invalid role")

# # teacher_service.py
# async def get_teacher_data(user: User):
#     # 선생님 데이터 처리 로직
#     return {"data": "teacher specific data"}


# # student_service.py
# async def get_student_data(user: User):
#     # 학생 데이터 처리 로직
#     return {"data": "student specific data"}