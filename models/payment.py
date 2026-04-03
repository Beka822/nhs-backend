from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Float,DateTime,ForeignKey
from datetime import datetime
import uuid
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.bill import Bill
from core.db import Base
class Payment(Base):
    __tablename__="payments"
    payment_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    bill_id:Mapped[str]=mapped_column(ForeignKey("bills.bill_id"),nullable=False,index=True)
    amount:Mapped[float]=mapped_column(Float,nullable=False)
    remaining:Mapped[float]=mapped_column(Float,nullable=True)
    payment_method:Mapped[str]=mapped_column(String,nullable=False)
    reference_number:Mapped[str|None]=mapped_column(String,nullable=True)
    received_by:Mapped[str]=mapped_column(String,nullable=False)
    received_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    bill:Mapped["Bill"]=relationship(back_populates="payments")
    