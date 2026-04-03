from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,DateTime,func
from core.db import Base
from datetime import datetime
class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    action:Mapped[str]=mapped_column(String,nullable=False)
    entity:Mapped[str]=mapped_column(String,nullable=False)
    entity_id:Mapped[str]=mapped_column(String,nullable=False)
    timestamp:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    