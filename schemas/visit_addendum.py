from pydantic import BaseModel
from datetime import datetime
class VisitAddendumCreate(BaseModel):
    patient_id:str
    visit_id:str
    comment:str
class VisitAddendumResponse(BaseModel):
    patient_id:str
    visit_id:str
    comment:str
    created_by:str
    created_at:datetime
    class Config:
        from_attributes=True
        
