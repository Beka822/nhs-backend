from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class DrugCreate(BaseModel):
    name:str
    category:Optional[str]=None
    unit:str
    buying_price:float
    selling_price:float
    quantity_in_stock:int=0
    reorder_level:int=10
    expiry_date:datetime | None=None
class DrugUpdate(BaseModel):
    name:Optional[str]=None
    category:Optional[str]=None
    unit:Optional[str]=None
    buying_price:Optional[float]=None
    selling_price:Optional[float]=None
    quantity_in_stock:Optional[int]=None
    reorder_level:Optional[int]=None
    expiry_date:datetime | None=None
class DrugResponse(BaseModel):
    drug_id:int
    hospital_id:str
    name:str
    category:Optional[str]
    unit:str
    buying_price:float
    selling_price:float
    quantity_in_stock:int
    reorder_level:int
    expiry_date:datetime | None=None
    created_at:datetime
    class Config:
        from_attributes=True

