from sqlalchemy.orm import Session
from models.visit_addendum import VisitAddendum

from models.audit_log import AuditLog
def create_visit_addendum(db:Session,data,current_user):
    addendum=VisitAddendum(patient_id=data.patient_id,visit_id=data.visit_id,comment=data.comment,created_by=current_user["sub"])
    db.add(addendum)
    db.commit()
    db.refresh(addendum)
    audit=AuditLog(action="CREATE_ADDENDUM",entity="VisitAddendum",entity_id=f"{data.patient_id}:{data.visit_id}",)
    db.add(audit)
    db.commit()
    return addendum
def get_visit_addendum_for_patient(db:Session,patient_id:str,visit_id:str):
    return db.query(VisitAddendum).filter(VisitAddendum.patient_id==patient_id,VisitAddendum.visit_id==visit_id).all()
def get_all_visit_addenda_by_patient(db:Session,patient_id:str):
    return db.query(VisitAddendum).filter(VisitAddendum.patient_id==patient_id).all()
