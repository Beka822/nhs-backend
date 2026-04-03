from pydantic import BaseModel
from datetime import datetime
from typing import Optional,Union
class VisitCreate(BaseModel):
    hospital_id:str
    patient_id:str
    symptoms:str
    diagnosis:str
    treatment:str
    notes:str|None=None
    payment_status:str
class VisitResponse(BaseModel):
    visit_id:str
    patient_id:str
    symptoms:str
    diagnosis:str
    treatment:str
    notes:str|None
    payment_status:str
    created_by:str
    created_at:datetime
    class Config:
        from_attributes=True
class VisitSuccess(BaseModel):
    status:str
    visit:Optional[VisitResponse]=None
    stk:Optional[dict]=None
ResponseModel=VisitSuccess
        