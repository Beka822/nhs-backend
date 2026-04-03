import logging
import sys
import json
import contextvars
correlation_id_var=contextvars.ContextVar("correlation_id",default=None)
class JsonFormatter(logging.Formatter):
    def format(self,record):
        log_record={"level":record.levelname,"message":record.getMessage(),"module":record.module,"time":self.formatTime(record),"correlation_id":correlation_id_var.get()}
        if record.exc_info:
            log_record["exception"]=self.formatException(record.exc_info)
        return json.dumps(log_record)
def setup_logging():
    handler=logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root_logger=logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers=[]
    root_logger.addHandler(handler)