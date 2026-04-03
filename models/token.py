from sqlalchemy import Column,String,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime,timedelta
import uuid
from core.db import Base
class RefreshToken(Base):
    __tablename__="refresh_tokens"
    token_id:Mapped[str]=mapped_column(primary_key=True,default=lambda:str(uuid.uuid4()),index=True)
    user_id:Mapped[str]=mapped_column(ForeignKey("user.user_id",nullable=False,index=True))
    hashed_token:Mapped[str]=mapped_column(nullable=False)
    created_at:Mapped[datetime]=mapped_column(default=datetime.utcnow)
    expires_at:Mapped[datetime]=mapped_column(default=lambda:datetime.utcnow()+timedelta(days=7))
    revoked:Mapped[bool]=mapped_column(default=False)
