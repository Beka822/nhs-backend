from sqlalchemy.orm import Session
from models.admission import Admission
from models.user import User
from models.bed import Bed
from models.audit_log import AuditLog
from models.transfer import Transfer
from models.notification import Notification
def transfer_patient(db:Session,admission_id:str,new_bed_id:str,reason:str,current_user:User,ip_address:str):
    if not reason.strip():
        raise ValueError("Transfer reason is mandatory")
    admission=db.query(Admission).filter(Admission.hospital_id==current_user.hospital_id,Admission.admission_id==admission_id,Admission.discharge_at.is_(None)).with_for_update().first()
    if not admission:
        raise ValueError("Admission not found")
    old_bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==admission.bed_id).with_for_update().first()
    new_bed=db.query(Bed).filter(Bed.hospital_id==current_user.hospital_id,Bed.bed_id==new_bed_id).with_for_update().first()
    if not new_bed:
        raise ValueError("New bed not found")
    if new_bed.status !="AVAILABLE":
        raise ValueError("New bed is not availble. may be occupied")
    if new_bed.is_icu and current_user.role != "DOCTOR":
        raise ValueError("Only doctors can transfer patients to ICU")
    old_bed.status="AVAILABLE"
    new_bed.status="OCCUPIED"
    admission.bed_id=new_bed_id
    transfer=Transfer(admission_id=admission_id,from_bed_id=old_bed.bed_id,to_bed_id=new_bed_id,reason=reason,transferred_by=current_user.user_id)
    db.add(transfer)
    db.flush()
    db.add(AuditLog(action="TRANSFER_PATIENT",entity="Transfer",entity_id=transfer.transfer_id))
    db.add(Notification(message=f"Patient moved from bed {old_bed.code} to {new_bed.code}"))
    db.commit()
    db.refresh(transfer)
    return transfer
    
    