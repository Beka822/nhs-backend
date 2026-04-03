from sqlalchemy import String,DateTime
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column
from core.db import Base
class Notification(Base):
    __tablename__="notifications"
    notification_id:Mapped[str]=mapped_column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    message:Mapped[str]=mapped_column(String,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    