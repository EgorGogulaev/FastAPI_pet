from fastapi import APIRouter

from .config import fastapi_users, auth_backend
from .schemas import UserRead, UserCreate, UserUpdate


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Auth"],
)