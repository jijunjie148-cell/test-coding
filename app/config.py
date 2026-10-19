from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    database_url: str = (
        "mysql+pymysql://taskflow:taskflow_dev@127.0.0.1:3306/taskflow?charset=utf8mb4"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
