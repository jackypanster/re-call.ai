from pydantic import BaseSettings, Field, ValidationError

class Settings(BaseSettings):
    api_host: str = Field(..., env="API_HOST")
    api_port: int = Field(..., env="API_PORT")
    debug: bool = Field(..., env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")

    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    preferred_model: str = Field(..., env="PREFERRED_MODEL")

    supermemory_api_key: str = Field(..., env="SUPERMEMORY_API_KEY")

    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")

    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

try:
    settings = Settings()
except ValidationError as e:
    print("❌ 环境变量配置错误：", e)
    raise
