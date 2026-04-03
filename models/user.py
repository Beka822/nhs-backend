from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,ForeignKey,Enum as SQLEnum
from models.hospital import Hospital
from core.db import Base
from enum import Enum
class UserRoles(str,Enum):
    SUPER_ADMIN="SUPER_ADMIN"
    NATIONAL_ADMIN="NATIONAL ADMIN"
    COUNTY_ADMIN="COUNTY ADMIN"
    ADMIN="ADMIN"
    DOCTOR="DOCTOR"
    NURSE="NURSE"
    STAFF="STAFF"
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id:Mapped[str]=mapped_column(String,unique=True,index=True,nullable=False)
    full_name:Mapped[str]=mapped_column(String,nullable=False)
    hashed_password:Mapped[str]=mapped_column(String,nullable=False)
    hospital_id:Mapped[str]=mapped_column(String,ForeignKey("hospitals.hospital_id"),nullable=True,index=True)
    hospital:Mapped["Hospital"]=relationship("Hospital",backref="users")
    role:Mapped[UserRoles]=mapped_column(SQLEnum(UserRoles,name="user_roles"),nullable=False)
    