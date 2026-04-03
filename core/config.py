from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60
    REDIS_URL:str
    FRONTEND_URLS:str
    ENVIRONMENT:str="development"
    FILE_ENCRYPTION_KEY:str
    MPESA_ENV:str
    MPESA_CONSUMER_KEY:str
    MPESA_CONSUMER_SECRET:str
    MPESA_SHORTCODE:str
    MPESA_PASSKEY:str
    MPESA_CALLBACK_URL:str
    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str
    AWS_BUCKET_NAME:str
    AWS_REGION:str
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",case_sensitive=True)
    
settings= Settings()