from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.security import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_jwt_token(token)
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
