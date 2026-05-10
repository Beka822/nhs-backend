from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,Numeric,DateTime,ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from core.db import Base
class Drug(Base):
    __tablename__="drugs"
    drug_id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    name:Mapped[str]=mapped_column(String,nullable=False)
    category:Mapped[str]=mapped_column(String)
    unit:Mapped[str]=mapped_column(String)
    buying_price:Mapped[float]=mapped_column(Numeric(10,2))
    selling_price:Mapped[float]=mapped_column(Numeric(10,2))
    quantity_in_stock:Mapped[int]=mapped_column(Integer,default=0)
    reorder_level:Mapped[int]=mapped_column(Integer,default=10)
    expiry_date:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)