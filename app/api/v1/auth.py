from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth_service import register_user, login_user

router= APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(request:RegisterRequest, session : AsyncSession = Depends(get_db)):
    try:
        return await register_user(session=session, email=request.email, password= request.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail= str(e))


@router.post("/login", response_model=TokenResponse)
async def login(request:LoginRequest, session: AsyncSession = Depends(get_db)):
    try:
        return await login_user(email=request.email, password=request.password, session= session)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))        

