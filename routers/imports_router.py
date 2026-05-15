import pandas as pd
from io import BytesIO
from fastapi import APIRouter,UploadFile,File,Depends
from sqlalchemy.orm import Session
from core.db import get_db
from core.dependencies import get_user_object
from models.user import User
from models.importing import ImportJob
router=APIRouter(prefix="/imports",tags=["Imports"])
@router.post("/upload")
async def upload_pharmacy_file(file:UploadFile=File(...),db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    filename=file.filename.lower()
    content=await file.read()
    if filename.endswith(".csv"):
        df=pd.read_csv(BytesIO(content))
    elif (
        filename.endswith(".xlsx")
        or
        filename.endswith(".xls")
    ):
        df=pd.read_excel(BytesIO(content))
    else:
        return{
            "error":
            "Unsupported file format"
        }
    job=ImportJob(hospital_id=current_user.hospital_id,file_name=file.filename,import_type="pharmacy",status="completed",total_rows=len(df))
    db.add(job)
    db.commit()
    db.refresh(job)
    return {
        "job_id":job.job_id,
        "file_name":file.filename,
        "columns":df.columns.tolist(),
        "total_rows":len(df),
        "preview":df.head(10).fillna("").to_dict(orient="records")
    }