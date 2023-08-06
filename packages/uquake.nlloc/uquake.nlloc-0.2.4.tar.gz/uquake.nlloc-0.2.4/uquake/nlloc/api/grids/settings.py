from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name = 'GRID_API'
    project_root: Optional[str] = None
    root: Optional[str] = None

    class Config:
        env_prefix: str = "GRID_"


settings = Settings()
