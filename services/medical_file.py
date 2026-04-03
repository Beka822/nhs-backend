import os,uuid
from pathlib import Path
from datetime import datetime
from fastapi.responses import StreamingResponse
from io import BytesIO
import re
from sqlalchemy.orm import Session
from models.patient import Patient
from models.medical_file import MedicalFile
from models.audit_log import AuditLog
from fastapi import UploadFile,HTTPException
from core.encryption import fernet
import boto3
from core.config import settings
s3=boto3.client("s3",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_REGION)
ALLOWED_MIME=["application/pdf","image/png","image/jpeg"]
MAX_FILE_SIZE=10*1024*1024
async def create_medical_file(db:Session,patient_id:str,file:UploadFile,current_user:dict):
    #Handle versioning
    contents=await file.read()
    encrypted=fernet.encrypt(contents)
    file_size=len(contents)
    if file_size>MAX_FILE_SIZE:
        raise HTTPException(400,detail="File too large")
    #await file.seek(0)
    file_id=f"MF-{uuid.uuid4().hex[:8]}"
    last_version=db.query(MedicalFile).filter(MedicalFile.patient_id==patient_id,MedicalFile.file_name==file.filename).order_by(MedicalFile.version.desc()).first()
    version=(last_version.version+1) if last_version else 1
    file_ext=Path(file.filename).suffix
    file_key=f"{patient_id}/{file_id}_v{version}{file_ext}"
    file_obj=BytesIO(encrypted)
    s3.upload_fileobj(file_obj,settings.AWS_BUCKET_NAME,file_key)
    medical_file=MedicalFile(file_id=file_id,file_name=file.filename,patient_id=patient_id,file_size=file_size,file_key=file_key,file_mime=file.content_type,uploaded_by=current_user["sub"],version=version,uploaded_at=datetime.utcnow())
    db.add(medical_file)
    db.commit()
    db.refresh(medical_file)
    audit=AuditLog(action="UPLOAD_FILE",entity="MedicalFile",entity_id=file_id)
    db.add(audit)
    db.commit()
    return medical_file
def download_medical_file(db:Session,patient_id:str,file_id:str,current_user:dict):
    """Return decrypted file path (or generated signed URL in cloud)"""
    medical_file=db.query(MedicalFile).filter(MedicalFile.file_id==file_id).first()
    if not medical_file or medical_file.patient_id != patient_id:
        raise ValueError("File not found")
    #update download metadata
    medical_file.downloaded_by=current_user["sub"]
    medical_file.downloaded_at=datetime.utcnow()
    db.commit()
    db.refresh(medical_file)
    audit=AuditLog(action="DOWNLOAD_FILE",entity="MedicalFile",entity_id=file_id)
    db.add(audit)
    db.commit()
    file_obj=BytesIO()
    s3.download_fileobj(settings.AWS_BUCKET_NAME,medical_file.file_key,file_obj)
    file_obj.seek(0)
    #encrypted_data=f.read()
    decrypted=fernet.decrypt(file_obj.read())
    return StreamingResponse(BytesIO(decrypted),media_type=medical_file.file_mime,headers={"Content-Disposition":f"attachment;filename={medical_file.file_name}"})
def get_medical_file_by_patient(db:Session,patient_id:str,current_user):
    patient=db.query(Patient).filter(Patient.patient_id==patient_id).first()
    if not patient:
        raise ValueError("Patient not found")
    files=(db.query(MedicalFile.file_id,MedicalFile.file_name).filter(MedicalFile.patient_id==patient_id).all())
    return files
    
    

