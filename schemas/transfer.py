from pydantic import BaseModel
from datetime import datetime
class TransferRequest(BaseModel):
    new_bed_id:str
    reason:str
class TransferResponse(BaseModel):
    transfer_id:str
    admission_id:str
    from_bed_id:str
    to_bed_id:str
    reason:str
    transferred_by:str
    transfer_time:datetime
    class Config:
        from_attributes=True
        