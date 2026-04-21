from sqlalchemy import String,DateTime,Float,Integer,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
from uuid import uuid4
from core.db import Base
class Pay(Base):
    __tablename__="pays"
    payment_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid4()),index=True)
    visit_id:Mapped[str]=mapped_column(String,ForeignKey("visits.visit_id"),index=True)
    phone_number:Mapped[str]=mapped_column(String,nullable=False)
    amount:Mapped[float]=mapped_column(Float)
    mpesa_receipt:Mapped[str]=mapped_column(String,unique=True,nullable=True)
    checkout_request_id:Mapped[str]=mapped_column(String,unique=True,nullable=True)
    reference:Mapped[str]=mapped_column(String)
    status:Mapped[str]=mapped_column(String)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    clinical_id:Mapped[str]=mapped_column(String)
    clinic_share:Mapped[int]=mapped_column(Integer,default=10)
