from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class AdmissionCreate(BaseModel):
    hospital_id:str
    patient_id:str
    bed_id:str
class AdmissionResponse(BaseModel):
    hospital_id:str
    visit_id:Optional[str]
    admission_id:str
    patient_id:str
    bed_id:str
    admitted_at:datetime
    discharged_at:Optional[datetime]|None=None
    class Config:
        from_attributes=True
