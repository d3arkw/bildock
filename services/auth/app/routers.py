from typing import Annotated

from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserCreate, UserOut
from bildock_lib.database import get_session
from bildock_lib.exceptions import ConflictError, UnauthorizedError
from bildock_lib.security import create_access_token, hash_password, verify_password
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register_user(db: Annotated[AsyncSession, Depends(get_session)], user_data: UserCreate):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    if user:
        raise ConflictError("User already exists")
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user:
        raise UnauthorizedError("Invalid email or password")
    if not verify_password(form_data.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
