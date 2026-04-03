import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,Boolean,ForeignKey
from typing import List,TYPE_CHECKING
if TYPE_CHECKING:
    from models.bed import Bed
    from models.hospital import Hospital

from core.db import Base
class Ward(Base):
    __tablename__="wards"
    ward_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"),nullable=False,index=True)
    code:Mapped[str]=mapped_column(String,unique=True,nullable=False)
    name:Mapped[str]=mapped_column(String,nullable=False)
    ward_type:Mapped[str]=mapped_column(String,nullable=False)
    capacity:Mapped[int]=mapped_column(Integer,nullable=False)
    floor:Mapped[str|None]=mapped_column(String,nullable=True)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    beds:Mapped[List["Bed"]]=relationship(back_populates="ward",cascade="all,delete-orphan")
    hospital=relationship("Hospital")

