from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import create_user, get_user_by_email
from app.core.security import hash_password, verify_password , create_access_token

async def register_user(session:AsyncSession, email: str, password:str)->dict:
    existing_user= get_user_by_email(session=session,email=email)
    
    if existing_user:
        raise ValueError("Email already registered")
    
    hashed_password= hash_password(password=password)
    user = await create_user(session=session, email=email, hashed_password=hashed_password)
    token = create_access_token(data={"sub":str(user.id)})
    
    return {
        "access_token":token,
        "token_type":"bearer"
    }

async def login(session:AsyncSession, email:str, password:str):
    existing_user=await get_user_by_email(session=session,email=email)
    
    if not existing_user:
        raise ValueError("Invalid email or password")
    if not verify_password(password, existing_user.hashedPassword):
        raise ValueError("Invalid email or password")
    
    if not existing_user.is_active:
        raise ValueError("Account is disabled")
    
    token = create_access_token(data={"sub":str(existing_user.id)})
    return {
        "access_token":token,
        "token_type":"bearer"
    }