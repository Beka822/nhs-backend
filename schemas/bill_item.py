from pydantic import BaseModel
class BillItemCreate(BaseModel):
    description:str
    quantity:int
    unit_price:float
class BillItemResponse(BaseModel):
    item_id:str
    bill_id:str
    description:str
    quantity:int
    unit_price:float
    total_price:float
    class Config:
        from_attributes=True