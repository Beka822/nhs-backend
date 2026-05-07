from sqlalchemy import String,Integer,Numeric,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column
from core.db import Base
class PharmacySale(Base):
    __tablename__="pharmacy_sales"
    sale_id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    drug_id:Mapped[int]=mapped_column(ForeignKey("drugs.drug_id"))
    quantity:Mapped[int]=mapped_column(Integer,nullable=False)
    total_price:Mapped[float]=mapped_column(Numeric,nullable=False)
    payment_method:Mapped[str]=mapped_column(String)
    sold_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)