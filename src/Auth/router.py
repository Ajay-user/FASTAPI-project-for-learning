from datetime import timedelta

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import User, CreateUser, UserCred
from .service import UserService
from .utils import verify_password, create_jwt_token
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

@auth_router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(user_cred:UserCred, session:AsyncSession=Depends(get_session)):
    user:User = await user_service.get_user_by_email(email=user_cred.email, session=session)
    if user:    
        password_match = verify_password(password=user_cred.password, hash=user.password)
        if password_match:

            user_data = {
                'user' : {
                    'email': user_cred.email,
                    'uid': str(user.uid)

                },
            }
            access_token = create_jwt_token(user_data=user_data)
            refresh_token = create_jwt_token(user_data=user_data, expire_delta=timedelta(minutes=1))

            return JSONResponse(
                content={
                    'message':'login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user_data
                }, 
            
                status_code=status.HTTP_202_ACCEPTED,
            )
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Password does not match')

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User does not exist')