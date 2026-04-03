from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from typing import Union
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
from core.security import SECRET_KEY,ALGORITHM
security=HTTPBearer()
def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
def get_user_object(payload:dict=Depends(get_current_user),db:Session=Depends(get_db))->User:
    user_id:str=payload.get("sub")
    
    role:str=payload.get("role")
    if not user_id:
        raise HTTPException(401,detail="Invalid token")
    user=db.query(User).filter(User.user_id==user_id).first()
    if not user:
        raise HTTPException(401,"Invalid credentials")
    return user
    
    
    
