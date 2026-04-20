from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

class DuplicateError(Exception):
    def __init__(self, message: str):
        self.message = message

class UnauthorizedError(Exception):
    def __init__(self, message: str):
        self.message = message

class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
       
        
        
def register_exception_handlers(app:FastAPI):
    
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail":exc.message}
        )
    
    @app.exception_handler(DuplicateError)
    async def duplicate_handler(request: Request, exc: DuplicateError):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )
    
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=401,
            content={"detail": exc.message}
        )
        
    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.message}
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )