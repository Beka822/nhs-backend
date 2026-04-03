from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class BedCreateRequest(BaseModel):
    
    ward_id:str
    code:str
    is_icu:Optional[bool]=False
class BedResponse(BaseModel):
    bed_id:str
    ward_id:str
    code:str
    status:str
    is_icu:bool
    created_at:datetime
    class Config:
        from_attributes=True