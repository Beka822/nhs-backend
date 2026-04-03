from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import (String,Integer,Text,DateTime,ForeignKey,UniqueConstraint,func,Index)
from datetime import datetime
import uuid
from core.db import Base
class Visit(Base):
    __tablename__="visits"
    __table_args__=(UniqueConstraint("patient_id","visit_id",name="uq_patient_visit"),)
    hospital_id:Mapped[str]=mapped_column(String,ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    visit_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda: "VIS-" + uuid.uuid4().hex[:6].upper(),nullable=False,index=True)
    patient_id:Mapped[str]=mapped_column(String,ForeignKey("patients.patient_id"),nullable=False,index=True)
    symptoms:Mapped[str]=mapped_column(Text,nullable=False)
    diagnosis:Mapped[str]=mapped_column(Text,nullable=False)
    treatment:Mapped[str]=mapped_column(Text,nullable=False)
    notes:Mapped[str]=mapped_column(Text,nullable=True)
    payment_status:Mapped[str]=mapped_column(String,default="PENDING")
    status:Mapped[str]=mapped_column(String,default="ACTIVE")
    created_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),nullable=False,index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    __table_args__=(Index("idx_visit_hospital","hospital_id"),Index("idx_visit_date","created_at"),Index("idx_visit_hospital_date","hospital_id","created_at"))
    
    