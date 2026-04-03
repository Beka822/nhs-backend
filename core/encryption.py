from cryptography.fernet import Fernet
from core.config import settings
fernet=Fernet(settings.FILE_ENCRYPTION_KEY.encode())