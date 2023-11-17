from fastapi import APIRouter, Depends
from fastapi import HTTPException

from app.utils.password import compare_passwords

from app.schemas.user import (
    UserCreateProtected,
    UserUpdateProtected,
    UserInDBProtected,
)
from app.schemas.password import Password

from app.controllers import user as user_controller
from app.messages import user as user_messages

from app.utils.deps import identify_request


api = APIRouter()


@api.get('/', response_model=UserInDBProtected)
async def get_by_id(
    user_id: int
):
    if user := await user_controller.get_by_id(user_id):
        return user
    else:
        raise HTTPException(404)


@api.post('/', response_model=UserInDBProtected)
async def create_user(
    user_data: UserCreateProtected,
):
    if user := await user_controller.save(user_data):
        await user_messages.emit_created(user)
        return user
    else:
        raise HTTPException(404)


@api.put('/', response_model=UserInDBProtected)
async def update_user(
    user_data: UserUpdateProtected,
    identity: dict = Depends(identify_request),
):
    if user := await user_controller.update(
        identity['sub'],
        user_data,
    ):
        return user
    else:
        raise HTTPException(404)


@api.delete('/', response_model=UserInDBProtected)
async def delete_user(
    identity: dict = Depends(identify_request),
):
    if user := await user_controller.delete(identity['sub']):
        await user_messages.emit_deleted(user)
        return user
    else:
        raise HTTPException(404)


async def change_password(
    password: Password,
    identity: dict = Depends(identify_request)
):
    if user := await user_controller.set_password(
        identity['sub'],
        password
    ):
        return user
    else:
        raise HTTPException(404)


# @api.post('/email', response_model=UserInDBProtected)
# async def connect_email(
#     email: str,
#     identity: dict = Depends(identify_request),
# ):
#     if user := await user_controller.add_email(
#         identity['sub'],
#         email
#     ):
#         return user
#     else:
#         raise HTTPException(404)


# @api.delete('/email', response_model=UserInDBProtected)
# async def disconnect_email(
#     email: str,
#     identity: dict = Depends(identify_request),
# ):
#     if user := await user_controller.remove_email(
#         identity['sub'],
#         email,
#     ):
#         return user
#     else:
#         raise HTTPException(404)
