from pydantic import BaseModel
from typing import Optional
class ErrorDetail(BaseModel):
    code:str
    message:str
class ErrorResponse(BaseModel):
    success:bool =False
    error:ErrorDetail
    class Config:
        from_attributes=True