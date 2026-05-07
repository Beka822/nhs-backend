from pydantic import BaseModel
from datetime import datetime
class PharmacySaleCreate(BaseModel):
    drug_id:int
    quantity:int
    payment_method:str
class PharmacySaleResponse(BaseModel):
    sale_id:str
    drug_id:int
    quantity:int
    total_price:float
    payment_method:str
    sold_at:datetime
    class Config:
        from_attributes=True