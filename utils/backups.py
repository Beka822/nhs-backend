import subprocess
import logging
from datetime import datetime
from io import BytesIO
import tempfile
import boto3
from urllib.parse import urlparse
from cryptography.fernet import Fernet
from core.config import settings
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s %(message)s]")
s3=boto3.client("s3",endpoint_url=settings.R2_ENDPOINT,aws_access_key_id=settings.R2_ACCESS_KEY_ID,aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY)
fernet=Fernet(settings.FILE_ENCRYPTION_KEY)
def timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
def backup_postgres(db_name:str,db_user:str):
    try:
        logging.info("Starting Postgres backup...")
        with tempfile.NamedTemporaryFile() as tmp:
           CMD=f"pg_dump -U {db_user} -F c -b -v {db_name} -f {tmp.name}"
           subprocess.run(CMD,shell=True,check=True)
           tmp.seek(0)
           encrypted_data=fernet.encrypt(tmp.read())
        filename=f"backups/db/db_backup_{timestamp()}.dump.enc"
        s3.upload_fileobj(BytesIO(encrypted_data),settings.R2_BACKUP_BUCKET,filename)
        if not verify_backup(settings.R2_BACKUP_BUCKET,filename):
            raise Exception("Postgres backup verification failed!")
        logging.info(f"Postgres backup uploaded to S3:{filename}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Postgres backup failed: {e.stderr.decode()}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during Postgres backup: {e}")
        raise
def backup_medical_files(s3_prefix="backups/medical-files"):
    try:
        logging.info("Starting medical files backup...")
        response=s3.list_objects_v2(Bucket=settings.R2_BUCKET_NAME,Prefix="medical-files/")
        if "Contents" not in response:
            logging.info("No medical files found to backup.")
            return
        ts=timestamp()
        for obj in response["Contents"]:
            key=obj["Key"]
            filename=key.split("/")[-1]
            backup_key=f"{s3_prefix}/{ts}_{filename}"
            s3.copy_object(Bucket=settings.R2_BACKUP_BUCKET,CopySource={"Bucket":settings.R2_BUCKET_NAME,"Key":key},Key=backup_key)
            if not verify_backup(settings.R2_BACKUP_BUCKET,backup_key):
                raise Exception(f"File backup failed:{backup_key}")
            logging.info(f"Copied: {key} and {backup_key}")
        logging.info("All medical files backed up successfully.")
    except Exception  as e:
        logging.error(f"Medical files backup failed: {e}")
        raise
def verify_backup(bucket,key):
    try:
        response=s3.head_object(Bucket=bucket,Key=key)
        if response["ContentLength"]==0:
            raise Exception("Backup file is empty!")
        logging.info(f"Backup verified: {key}")
        return True
    except Exception as e:
        logging.error(f"Backup verification failed: {key} - {e}")
        return False
def run_all_backups():
    logging.info("Starting full cloud-native backup sequence...")
    db=urlparse(settings.DATABASE_URL)
    backup_postgres(db_name=db.path.lstrip("/")[-1],db_user=db.username.split(":")[1].split("@")[0])
    backup_medical_files()
    logging.info("Full cloud-native backup sequence completed successfully.")
if __name__ == "__main__":
    run_all_backups()
    