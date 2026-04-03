from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.logging import setup_logging
from core.exceptions import (app_exception_handler,validation_exception_handler,http_exception_handler,general_exception_handler,AppException)
from fastapi.exceptions import RequestValidationError
from core.middleware import CorrelationIdMiddleware
from core.db import Base,engine
from routers.hospital_router import router as hospital_router
from routers.user_router import router as user_router
from routers.auth_router import router as auth_router
from routers.patient_router import router as patient_router
from routers.visit_router import router as visit_router
from routers.visit_addendum_router import router as visit_addendum_router
from routers.medical_file_router import router as medical_file_router
from routers.ward_router import router as ward_router
from routers.beds_router import router as beds_router
from routers.admission_router import router as admission_router
from routers.transfer_router import router as transfer_router
from routers.bill_router import router as bill_router
from routers.bill_item_router import router as bill_item_router
from routers.payment_router import router as payment_router
from routers.pays_router import router as pays_router
from routers.wallet_router import router as wallet_router
from core.config import settings

setup_logging()
app=FastAPI(title="Universal Electronic Health System",description="Backend API for managing patients,visits,medical files, and healthcare operations.",version="1.0.0")

origins=settings.FRONTEND_URLS.split(",")
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

app.add_exception_handler(AppException,app_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(Exception,general_exception_handler)
app.add_middleware(CorrelationIdMiddleware)

Base.metadata.create_all(bind=engine)
app.include_router(hospital_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(visit_router)
app.include_router(visit_addendum_router)
app.include_router(medical_file_router)
app.include_router(ward_router)
app.include_router(beds_router)
app.include_router(admission_router)
app.include_router(transfer_router)
app.include_router(bill_router)
app.include_router(bill_item_router)
app.include_router(payment_router)
app.include_router(pays_router)
app.include_router(wallet_router)













