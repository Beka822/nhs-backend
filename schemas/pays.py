from pydantic import BaseModel
class RevenueResponse(BaseModel):
    hospital_name:str
    total_visits:int
    total_revenue:int
    clinic_earnings:int
    month:str
    class Config:
        from_attributes=True