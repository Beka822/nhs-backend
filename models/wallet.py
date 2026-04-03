from sqlalchemy import String,Float,DateTime,ForeignKey
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Mapped,mapped_column
from core.db import Base
class Wallet(Base):
    __tablename__="wallets"
    wallet_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()),index=True)
    patient_id:Mapped[str]=mapped_column(String,ForeignKey("patients.patient_id"))
    balance:Mapped[float]=mapped_column(Float,default=0)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class WalletTransaction(Base):
    __tablename__="wallet_transactions"
    transaction_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    wallet_id:Mapped[str]=mapped_column(String,ForeignKey("wallets.wallet_id"))
    amount:Mapped[float]=mapped_column(Float)
    transaction_type:Mapped[str]=mapped_column(String)
    reference:Mapped[str]=mapped_column(String)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)