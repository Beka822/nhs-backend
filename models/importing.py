from core.db import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,String,Integer,DateTime
from datetime import datetime
class ImportJob(Base):
    __tablename__="import_jobs"
    job_id:Mapped[int]=mapped_column(primary_key=True,index=True)
    hospital_id:Mapped[str]=mapped_column(ForeignKey("hospitals.hospital_id"))
    file_name:Mapped[str]
    import_type:Mapped[str]
    status:Mapped[str]=mapped_column(default="processing")
    total_rows:Mapped[int]=mapped_column(default=0)
    created_at:Mapped[datetime]=mapped_column(default=datetime.utcnow)