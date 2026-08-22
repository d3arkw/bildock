from typing import Annotated

from app.models import User
from bildock_lib.database import get_session
from bildock_lib.exceptions import UnauthorizedError
from bildock_lib.security import decode_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(db: Annotated[AsyncSession, Depends(get_session)], token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
    except ValueError:
        raise UnauthorizedError("Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Unauthorized")
    if not user_id.isdigit():
        raise UnauthorizedError("Invalid or expired token")
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    if not user:
        raise UnauthorizedError("User not found")
    return user
