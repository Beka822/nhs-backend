from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import (String,Integer,DateTime,Float,ForeignKey,func)
from core.db import Base
from datetime import datetime
class MedicalFile(Base):
    __tablename__="medical_files"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    file_id:Mapped[str]=mapped_column(String,unique=True,nullable=False,index=True)
    file_name:Mapped[str]=mapped_column(String,nullable=True)
    patient_id:Mapped[str]=mapped_column(String,ForeignKey("patients.patient_id"),nullable=False,index=True)
    file_size:Mapped[float]=mapped_column(Float,nullable=False)
    file_key:Mapped[str]=mapped_column(String,nullable=False)
    file_mime:Mapped[str]=mapped_column(String,nullable=False)
    uploaded_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),nullable=False,index=True)
    downloaded_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),nullable=True,index=True)
    uploaded_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    downloaded_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=True)
    version:Mapped[int]=mapped_column(Integer,nullable=False,default=1)
    
