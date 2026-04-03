from pydantic import BaseModel
from typing import Optional
class WardCreate(BaseModel):
    
    code:str

    name:str
    ward_type:str
    capacity:int
    floor:str|None
class WardUpdate(BaseModel):
    name:Optional[str]=None
    ward_type:Optional[str]=None
    capacity:Optional[str]=None
    is_active:Optional[bool]=None
    floor:Optional[str]=None
class WardResponse(BaseModel):
    
    ward_id:str
    name:str
    ward_type:str
    capacity:int
    is_active:bool
    floor:str|None
    class Config:
        from_attributes=True
        