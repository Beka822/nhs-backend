from pydantic import BaseModel
from datetime import datetime
class MedicalFileUpload(BaseModel):
    patient_id:str
    file_id:str
    file_name:str
    file_mime:str
    file_size:float
class MedicalFileResponse(BaseModel):
    file_id:str
    file_name:str
    patient_id:str
    file_path:str
    file_size:float
    file_mime:str
    uploaded_by:str
    uploaded_at:datetime
    downloaded_by:str|None
    downloaded_at:datetime|None
    version:int
    class Config:
        from_attributes=True
class MedicalFileListResponse(BaseModel):
    file_id:str
    file_name:str
    class Config:
        from_attributes=True
        
        