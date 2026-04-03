from sqlalchemy import String,Float,ForeignKey,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
import uuid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.payment import Payment
from core.db import Base
class Bill(Base):
    __tablename__="bills"
    bill_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    visit_id:Mapped[str]=mapped_column(ForeignKey("visits.visit_id"),index=True,nullable=False)
    admission_id:Mapped[str| None]=mapped_column(ForeignKey("admissions.admission_id"),index=True,nullable=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    patient_id:Mapped[str]=mapped_column(ForeignKey("patients.patient_id"),index=True)
    total_amount:Mapped[float]=mapped_column(Float,nullable=False)
    amount_paid:Mapped[float]=mapped_column(Float,default=0.0)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    paid_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    payments:Mapped[list["Payment"]]=relationship(back_populates="bill",cascade="all,delete-orphan")
    
    