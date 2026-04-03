import os
import subprocess
import shutil
from datetime import datetime
import logging
LOG_DIR="/logs"
os.makedirs(LOG_DIR,exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR,"backup.log"),level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")
def backup_postgres(db_name:str,db_user:str,backup_dir:str="/backups/postgres"):
    try:
        os.makedirs(backup_dir,exist_ok=True)
        timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M")
        backup_file=os.path.join(backup_dir,f"full_backup_{timestamp}.dump")
        cmd=f"pg_dump -U {db_user} -F c -b -v -f {backup_file} {db_name}"
        subprocess.run(cmd,shell=True,check=True)
        logging.info(f"PostgreSQL backup completed: {backup_file}")
    except Exception as e:
        logging.error(f"PostgreSQL backup failed: {e}")
def backup_medical_files(source_dir="/media/patient_files",backup_dir="/backups/patient_files"):
    try:
        os.makedirs(backup_dir,exist_ok=True)
        timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M")
        target_dir=os.path.join(backup_dir,f"backup_{timestamp}")
        shutil.copytree(source_dir,target_dir)
        logging.info(f"Medical files backup completed: {target_dir}")
    except Exception as e:
        logging.error(f"Medical files backup failed: {e}")
def run_all_backups():
    logging.info("Starting full backup sequence...")
    backup_postgres(db_name=os.getenv("DB_NAME","hospital_db"),db_user=os.getenv("DB_USER","postgres"))
    backup_medical_files(source_dir=os.getenv("MEDICAL_FILES_PATH","/media/patient_files"))
    logging.info("Full backup sequence completed successfully.")