from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    app_description: str
    database_url: str
    archives_save_path: str

    class Config:
        env_file = ".env"


settings = Settings()
