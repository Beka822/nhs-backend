from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError 
import logging
from core.error_schema import ErrorResponse
logger=logging.getLogger(__name__)
class AppException(Exception):
    def __init__(self,code:str,message:str,status_code:int=400):
        self.code=code
        self.message=message
        self.status_code=status_code
class ResourceNotFound(AppException):
    def __init__(self,resource:str):
        super().__init__(code="RESOURCE_NOT_FOUND",message=f"{resource} not found",status_code=404)
class UnauthorizedAccess(AppException):
    def __init__(self):
        super().__init__(code="UNAUTHORIZED",message="You are not authorized to perform this action",status_code=403)
async def app_exception_handler(request:Request,exc:AppException):
    correlation_id=getattr(request.state,"correlation_id","N/A")
    logger.warning(f"[CID:{correlation_id}] {exc.code} | Path: {request.url}")
    return JSONResponse(status_code=exc.status_code,content=ErrorResponse(error={"code": exc.code,"message": exc.message}).model_dump())
async def validation_exception_handler(request:Request,exc:RequestValidationError):
    logger.warning(f"Validation error at {request.url}")
    return JSONResponse(status_code=422,content=ErrorResponse(error={"code": "VALIDATION_ERROR","message":"Invalid request data"}).model_dump())
async def http_exception_handler(request:Request,exc:HTTPException):
    logger.warning(f"HTTP error {exc.status_code} at {request.url}")
    return JSONResponse(status_code=exc.status_code,content=ErrorResponse(error={"code": "HTTP_ERROR","message": exc.detail}).model_dump())
async def general_exception_handler(request:Request,exc:Exception):
    logger.exception(f"Unhandled error at {request.url}")
    return JSONResponse(status_code=500,content=ErrorResponse(error={"code": "INTERNAL_SERVER_ERROR","message": "Something went wrong"}).model_dump())