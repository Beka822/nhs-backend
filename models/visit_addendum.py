from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import (String,Integer,Text,DateTime,ForeignKey,ForeignKeyConstraint,func)
from core.db import Base
from datetime import datetime
class VisitAddendum(Base):
    __tablename__="visit_addenda"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    patient_id:Mapped[str]=mapped_column(String,nullable=False)
    visit_id:Mapped[str]=mapped_column(String,nullable=False)
    comment:Mapped[str]=mapped_column(Text,nullable=False)
    created_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),nullable=False,index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    __table_args__=(ForeignKeyConstraint(["patient_id","visit_id"],["visits.patient_id","visits.visit_id"],),)
    