from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import register_user, login_user

router= APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(request:RegisterRequest, session : AsyncSession = Depends(get_db)):
    return await register_user(session=session, email=request.email, password= request.password)


@router.post("/login", response_model=TokenResponse)
async def login(request:LoginRequest, session: AsyncSession = Depends(get_db)):
    return await login_user(email=request.email, password=request.password, session= session)

