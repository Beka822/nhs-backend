from sqlalchemy import String,Integer,DateTime,func
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
from core.db import Base
class Hospital(Base):
    __tablename__="hospitals"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    hospital_id:Mapped[str]=mapped_column(String,unique=True,index=True,nullable=False)
    hospital_name:Mapped[str]=mapped_column(String,nullable=False)
    county:Mapped[str]=mapped_column(String,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())