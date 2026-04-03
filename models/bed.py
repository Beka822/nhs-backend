import uuid
from sqlalchemy import ForeignKey,DateTime,String,Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import List,TYPE_CHECKING
if TYPE_CHECKING:
    from models.ward import Ward
    from models.admission import Admission

from core.db import Base
class Bed(Base):
    __tablename__="beds"
    bed_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    code:Mapped[str]=mapped_column(String,unique=True,nullable=False)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    ward_id:Mapped[str]=mapped_column(ForeignKey("wards.ward_id"),nullable=False,index=True)
    status:Mapped[str]=mapped_column(String,default="AVAILABLE")
    is_icu:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    ward:Mapped["Ward"]=relationship(back_populates="beds")
    admissions:Mapped[List["Admission"]]=relationship(back_populates="bed")
