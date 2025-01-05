import json
from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.system.database.connection import get_db
from app.views.users.models import User
from app.views.users.repository import UserRepository
from app.views.users.schemas import CreateUserSchema, ResponseUserSchema, UpdateUserSchema


router = APIRouter(
    tags=['users']
)

@router.post("/",status_code= HTTPStatus.CREATED, summary="Endpoint for create user", response_model=ResponseUserSchema)
async def create_user(user: CreateUserSchema, db: AsyncSession = Depends(get_db)):
    new_user = User(**user.model_dump())
    exists_user = await UserRepository(db=db).get_by_email(email=new_user.email)
    if exists_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email already registered")
    saved_user = await new_user.save(session=db)
    return ResponseUserSchema(**saved_user.to_dict())


@router.get("/{user_id}", status_code=HTTPStatus.OK, summary="Endpoint for get user by id", response_model=ResponseUserSchema)
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
    user_uuid = UserRepository.validate_uuid_format(user_id)

    user = await UserRepository(db=db).get_by_id(id=user_uuid)
    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User not found.")
    return ResponseUserSchema(**user.to_dict())

@router.patch('/update/{user_id}', status_code=HTTPStatus.OK, summary="Endpoint for edit user by id", response_model=ResponseUserSchema)
async def update_user(user_id: str, user_update_data: UpdateUserSchema, db: AsyncSession = Depends(get_db)):
    user_uuid = UserRepository.validate_uuid_format(user_id)
    updated_user = await UserRepository(db).update_user(user_uuid, user_update_data)
    return ResponseUserSchema(**updated_user.to_dict())

@router.delete('/delete/{user_id}', status_code=HTTPStatus.OK, summary="Endpoint for delete user by id")
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    await UserRepository(db).delete_user(user_id)
    return {"message": "Request was successful!"}
