from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import create_user, get_user_by_email
from app.core.security import hash_password, verify_password , create_access_token
from app.core.exceptions import DuplicateError, UnauthorizedError

async def register_user(session:AsyncSession, email: str, password:str)->dict:
    existing_user=await get_user_by_email(session=session,email=email)
    if existing_user:
        raise DuplicateError("Email already registered")

    hashed_password= hash_password(password=password)
    user = await create_user(session=session, email=email, hashed_password=hashed_password)
    token = create_access_token(data={"sub":str(user.id)})

    return {
        "access_token":token,
        "token_type":"bearer"
    }

async def login_user(session:AsyncSession, email:str, password:str):
    existing_user=await get_user_by_email(session=session,email=email)

    if not existing_user:
        raise UnauthorizedError("Invalid email or password")
    if not verify_password(password, existing_user.hashed_password):
        raise UnauthorizedError("Invalid email or password")

    if not existing_user.is_active:
        raise UnauthorizedError("Account is disabled")

    token = create_access_token(data={"sub":str(existing_user.id)})
    return {
        "access_token":token,
        "token_type":"bearer"
    }