from sqlalchemy import ForeignKey,DateTime,String,Float,Integer
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
import uuid
from core.db import Base
class BillItem(Base):
    __tablename__="bill_items"
    item_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),nullable=False,index=True)
    bill_id:Mapped[str]=mapped_column(String,ForeignKey("bills.bill_id"),index=True)
    description:Mapped[str]=mapped_column(String)
    quantity:Mapped[int]=mapped_column(Integer)
    unit_price:Mapped[float]=mapped_column(Float)
    total_price:Mapped[float]=mapped_column(Float)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    