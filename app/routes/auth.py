from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
def register():
    return {"message": "User registered successfully"}


@router.post("/login")
def login():
    token = create_access_token({"sub": "demo-user"})
    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    return {
        "message": "Current user",
        "token": token,
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}