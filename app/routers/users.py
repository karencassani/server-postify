from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import select
from app.schemas.post import PostRead

from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

from app.db.session import get_session
import uuid
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=List[UserRead])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User)) 
    return result.scalars().all()

@router.post('/', response_model=UserRead, status_code= 201)
async def create_user(data: UserCreate, session: AsyncSession= Depends(get_session)):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: uuid.UUID, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.get('/{userId}/posts', response_model=List[PostRead], status_code=200)
async def get_posts_by_user(userId: uuid.UUID, session: AsyncSession = Depends(get_session)):
    res= await session.execute(select(Post).where(Post.user_id == user_id))
    return res.scalars().all()

