from sqlalchemy import String,DateTime,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime
import uuid
from core.db import Base
class Transfer(Base):
    __tablename__="transfers"
    transfer_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    admission_id:Mapped[str]=mapped_column(ForeignKey("admissions.admission_id"),nullable=False,index=True)
    from_bed_id:Mapped[str]=mapped_column(ForeignKey("beds.bed_id"),nullable=False,index=True)
    to_bed_id:Mapped[str]=mapped_column(ForeignKey("beds.bed_id"),nullable=False,index=True)
    reason:Mapped[str]=mapped_column(String,nullable=False)
    transferred_by:Mapped[str]=mapped_column(String,ForeignKey("users.user_id"),index=True)
    transfer_time:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    