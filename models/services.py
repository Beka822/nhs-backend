from core.db import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,ForeignKey,Float,DateTime
import uuid
from datetime import datetime
class Service(Base):
    __tablename__="services"
    service_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),index=True,nullable=False)
    name:Mapped[str]=mapped_column(String,nullable=False)
    price:Mapped[float]=mapped_column(Float,nullable=False)
    is_active:Mapped[bool]=mapped_column(default=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)