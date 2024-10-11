from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class ServerSettings(BaseModel):
    LOCALHOST: str
    PORT: int

class Settings(BaseSettings):
    server: ServerSettings

    model_config = SettingsConfigDict(toml_file="config.toml")