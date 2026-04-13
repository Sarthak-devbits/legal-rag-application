from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config= SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str ="development"
    secret_key:str
    access_token_expire_minutes: int = 60
    database_url: str
    rabbitmq_url: str
    redis_url:str
    minio_endpoint:str
    minio_access_key:str
    minio_secret_key:str
    minio_bucket: str = "legal_docs"
    minio_secure: bool = False
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o"
    cohere_api_key: str = ""
    celery_ingestion_concurrency: int = 2
    celery_query_concurrency: int = 4

settings = Settings()