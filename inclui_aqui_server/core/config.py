from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings for the inclui server application.
    """

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: str
    PROJECT_NAME: str
    API_V1_STR: str
    
# Cria uma instância única que será importada em todo o projeto
settings = Settings()