import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from core.logging import correlation_id_var
logger=logging.getLogger(__name__)
class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        correlation_id=str(uuid.uuid4())
        correlation_id_var.set(correlation_id)
        response=await call_next(request)
        response.headers["X-Correlation-ID"]=correlation_id
        return response