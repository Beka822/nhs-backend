from pydantic import BaseModel
from datetime import datetime
class PaymentCreate(BaseModel):
    amount:float
    payment_method:str
    reference_number:str|None=None
class PaymentResponse(BaseModel):
    payment_id:str
    bill_id:str
    amount:float
    remaining:float|None
    payment_method:str
    reference_number:str|None
    received_by:str
    received_at:datetime
    class Config:
        from_attributes=True
        

