from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,String,DateTime,ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.bed import Bed
import uuid
from core.db import Base
class Admission(Base):
    __tablename__="admissions"
    
    admission_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),unique=True,index=True)
    patient_id:Mapped[str]=mapped_column(ForeignKey("patients.patient_id"),nullable=False,index=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    visit_id:Mapped[str]=mapped_column(ForeignKey("visits.visit_id"),nullable=True,index=True)
    bed_id:Mapped[str]=mapped_column(ForeignKey("beds.bed_id"),nullable=False,index=True)
    admitted_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    discharge_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    created_by:Mapped[str]=mapped_column(ForeignKey("users.user_id"),nullable=False,index=True)
    bed:Mapped["Bed"]=relationship("Bed",back_populates="admissions")
    

