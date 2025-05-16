from datetime import timedelta,datetime

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import User, CreateUser, UserCred
from .service import UserService
from .utils import verify_password, create_jwt_token
from .dependency import RefreshTokenHandler, AccessTokenHandler
from db.main import get_session
from db.redis import add_jwt_id_to_block_list



auth_router = APIRouter()
user_service = UserService()
refresh_handler = RefreshTokenHandler()
access_handler = AccessTokenHandler()



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
                    'uid': str(user.uid),

                },
            }
            access_token = create_jwt_token(user_data=user_data)
            refresh_token = create_jwt_token(user_data=user_data, expire_delta=timedelta(minutes=5), refresh=True)

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


@auth_router.post(path="/refresh_token")
def get_new_token(user_data:dict=Depends(refresh_handler)):
    '''Create new token after validating the refresh token'''
    if datetime.fromtimestamp(user_data['exp']) > datetime.now():
        new_token = create_jwt_token(user_data=user_data)
        return JSONResponse(content={
            'message':"refresh token accepted, issuing new access token",
            'access_token': new_token,
            'user': user_data,
            'refresh': True
        })
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired, Login required")


@auth_router.post(path='/logout') 
async def logout_user(user_data:dict=Depends(access_handler)):
    jid = user_data['jid']
    await add_jwt_id_to_block_list(jid=jid)
    return JSONResponse(
        content={'message':"Logged out successfully"},
        status_code=status.HTTP_200_OK
    )

