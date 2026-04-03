from core.db import SessionLocal
from models.user import User
from core.security import hash_password
db=SessionLocal()
super_admin=User(user_id="Ad-002",full_name="Beka Eli",hospital_id=None,role="SUPER_ADMIN",hashed_password=hash_password("Ad254"))
db.add(super_admin)
db.commit()
db.close()