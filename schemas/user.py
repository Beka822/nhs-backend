from pydantic import BaseModel
from models.user import UserRoles
class UserCreate(BaseModel):
    user_id:str
    full_name:str
    hospital_id:str
    role:UserRoles
    password:str
class UserResponse(BaseModel):
    user_id:str
    full_name:str
    hospital_id:str
    role:UserRoles
    class Config:
        from_attributes=True