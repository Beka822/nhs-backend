from pydantic import BaseModel
from datetime import date,datetime
from typing import List
from models.patient import Gender
class PatientCreate(BaseModel):
    patient_id:str
    patient_name:str
    date_of_birth:date
    gender:Gender
    phone:str
class PatientResponse(BaseModel):
    patient_id:str
    patient_name:str
    date_of_birth:date
    gender:Gender
    phone:str
    created_at:datetime
    created_by:str
    class Config:
        from_attributes=True
class PatientPagResponse(BaseModel):
    page:int
    page_size:int
    total:int
    items:List[PatientResponse]


        