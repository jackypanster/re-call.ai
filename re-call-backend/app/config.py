from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    secret_key: str
    mem0_api_key: str
    openai_api_key: str = ""
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
