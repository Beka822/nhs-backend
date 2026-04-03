from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class WalletResponse(BaseModel):
    wallet_id:str
    patient_id:str
    balance:float
    class Config:
        from_attributes=True
class WalletTransactionResponse(BaseModel):
    transaction_id:str
    amount:float
    transaction_type:str
    reference:str
    created_at:datetime
    class Config:
        from_attributes=True
class WalletTopUpRequest(BaseModel):
    phone_number:str
    amount:float
    reference:Optional[str]=None
