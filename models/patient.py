from enum import Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,Date,DateTime,Enum as SQLEnum,ForeignKey,func
from core.db import Base
from datetime import datetime,date
class Gender(str,Enum):
    MALE="MALE"
    FEMALE="FEMALE"
    OTHER="OTHER"
class Patient(Base):
    __tablename__="patients"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    patient_id:Mapped[str]=mapped_column(String,unique=True,index=True,nullable=False)
    patient_name:Mapped[str]=mapped_column(String,nullable=False)
    date_of_birth:Mapped[date]=mapped_column(Date,nullable=False)
    gender:Mapped[Gender]=mapped_column(SQLEnum(Gender,name="gender_enum"),nullable=False)
    phone:Mapped[str]=mapped_column(String,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    created_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),nullable=False,index=True)