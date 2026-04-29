from pydantic import BaseModel,Field
class ServiceCreate(BaseModel):
    name:str=Field(...,min_length=2)
    price:float=Field(...,gt=0)