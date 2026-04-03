from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import computed_field
class BillCreate(BaseModel):
    hospital_id:str
    admission_id:Optional[str]=None
class BillPayment(BaseModel):
    amount_paid:float
class BillResponse(BaseModel):
    bill_id:str
    admission_id:Optional[str]
    patient_id:str
    patient_name:str
    total_amount:float
    amount_paid:float
    created_at:datetime
    paid_at:datetime|None
    class Config:
        from_attributes=True
        @computed_field
        @property
        def status(self)->str:
            if self.amount_paid==0:
                return "UNPAID"
            elif self.amount_paid<self.total_amount:
                return "PARTIAL"
            else:
                return "PAID"
            

        