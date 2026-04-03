from fastapi import APIRouter,Depends,UploadFile,HTTPException,File
from sqlalchemy.orm import Session
from schemas.medical_file import MedicalFileListResponse
from core.db import get_db
from services.medical_file import create_medical_file,download_medical_file,get_medical_file_by_patient
from core.permissions import require_roles
router=APIRouter(prefix="/medical-files",tags=["Medical Files"])
@router.post("/upload/{patient_id}")
async def upload_file(patient_id:str,file:UploadFile=File(...),db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    try:
        medical_file=await create_medical_file(db,patient_id,file,current_user)
        return  {"message":"File uploaded successfully","file_id":medical_file.file_id,"version":medical_file.version}
    except ValueError as e:
        raise HTTPException(400,detail=str(e))
@router.get("/download/{patient_id}/{file_id}")
async def download_file(patient_id:str,file_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    try:
        return download_medical_file(db,patient_id,file_id,current_user)
    except ValueError as e:
        raise HTTPException(404,detail=str(e))
@router.get("/patient/{patient_id}",response_model=list[MedicalFileListResponse])
def get_medical_files(patient_id:str,db:Session=Depends(get_db),current_user:dict=Depends(require_roles("ADMIN","DOCTOR","NURSE"))):
    return get_medical_file_by_patient(db,patient_id,current_user)
    
    
