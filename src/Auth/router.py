from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import User, CreateUser
from .service import UserService
from db.main import get_session

auth_router = APIRouter()
user_service = UserService()



@auth_router.post('/signup',status_code=status.HTTP_201_CREATED)
async def signup(user:CreateUser, session:AsyncSession=Depends(get_session))->User:
    is_user = await user_service.is_user(email=user.email, session=session)

    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User already exists in database')
    user_ = await user_service.create_user(user=user, session=session)
    return user_