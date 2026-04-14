import subprocess
import boto3
from io import BytesIO
from cryptography.fernet import Fernet
from core.config import settings
s3=boto3.client("s3",endpoint_url=settings.R2_ENDPOINT,aws_access_key_id=settings.R2_ACCESS_KEY_ID,aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,)
fernet=Fernet(settings.FILE_ENCRYPTION_KEY)
def restore_postgres(backup_key,db_name,db_user):
    obj=s3.get_object(Bucket=settings.R2_BACKUP_BUCKET,Key=backup_key)
    encrypted_data=obj["Body"].read()
    decrypted_data=fernet.decrypt(encrypted_data)
    with open("restore.dump","wb") as f:
        f.write(decrypted_data)
    CMD=f"pg_restore -U {db_user} -d {db_name} restore.dump"
    subprocess.run(CMD,shell=True,check=True)
    print("Database restored successfully.")