from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import verify_password, hash_password
from .models import User as UserModel
from .schema import User


class UserService:

    async def get_user_by_email(self, email:str, session:AsyncSession)->UserModel:
        statement = select(UserModel).where(UserModel.email==email)
        result = await session.execute(statement=statement)
        user = result.scalar()
        return user

    async def is_user(self, email:str, session:AsyncSession)->bool:
        user:UserModel = await self.get_user_by_email(email=email, session=session)
        if user:
            return True
        return False
    
    async def create_user(self, user:User, session:AsyncSession)->UserModel:
        user_dict:dict = user.model_dump()
        user_dict['password'] = hash_password(user_dict['password'])
        user_model = UserModel(**user_dict)
        session.add(user_model)
        await session.commit()
        return user_model
