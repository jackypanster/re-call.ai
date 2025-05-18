from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool
    secret_key: str
    openrouter_api_key: str
    preferred_model: str
    supermemory_api_key: str
    supabase_url: str
    supabase_key: str
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

try:
    settings = Settings()
except Exception as e:
    print("❌ 环境变量配置错误：", e)
    raise
