from pydantic import BaseModel
from datetime import datetime
class HospitalCreate(BaseModel):
    hospital_id:str
    hospital_name:str
    county:str
class HospitalResponse(BaseModel):
    hospital_id:str
    hospital_name:str
    county:str
    created_at:datetime
    class Config:
        from_attributes=True
        