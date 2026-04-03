import subprocess
import logging
from datetime import datetime
from io import BytesIO
import boto3
from cryptography.fernet import Fernet
from core.config import settings
logging.basicConfig(filename="logs/backup.log",level=logging.INFO,format="%(asctime)s [%(levelname)s %(message)s]")
s3=boto3.client("s3",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_REGION)
fernet=Fernet(settings.FILE_ENCRYPTION_KEY)
def timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
def backup_postgres(db_name:str,db_user:str):
    try:
        logging.info("Starting Postgres backup...")
        CMD=f"pg_dump -U {db_user} -F c -b -v {db_name}"
        result=subprocess.run(CMD,shell=True,check=True,capture_output=True)
        encrypted_data=fernet.encrypt(result.stdout)
        filename=f"backups/db/db_backup_{timestamp()}.dump.enc"
        s3.upload_fileobj(BytesIO(encrypted_data),settings.AWS_BUCKET_NAME,filename)
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
        response=s3.list_objects_v2(Bucket=settings.AWS_BUCKET_NAME,Prefix="medical-files/")
        if "Contents" not in response:
            logging.info("No medical files found to backup.")
            return
        for obj in response["Contents"]:
            key=obj["Key"]
            file_obj=BytesIO()
            s3.download_fileobj(settings.AWS_BUCKET_NAME,key,file_obj)
            file_obj.seek(0)
            filename=key.split("/")[-1]
            backup_key=f"{s3_prefix}/{timestamp()}_{filename}"
            s3.upload_fileobj(file_obj,settings.AWS_BUCKET_NAME,backup_key)
            logging.info(f"Medical file backend up in S3: {backup_key}")
        logging.info("All medical files backed up successfully.")
    except Exception  as e:
        logging.error(f"Medical files backup failed: {e}")
        raise
def run_all_backups():
    logging.info("Starting full cloud-native backup sequence...")
    backup_postgres(db_name=settings.DATABASE_URL.split("/")[-1],db_user=settings.DATABASE_URL.split(":")[1].split("@")[0])
    backup_medical_files()
    logging.info("Full cloud-native backup sequence completed successfully.")
if __name__ == "__main__":
    run_all_backups()
    