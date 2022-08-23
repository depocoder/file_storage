"""Settings module."""
import os
import pathlib
from tempfile import gettempdir

from environs import Env
from pydantic import BaseSettings
from yarl import URL

env = Env()
env.read_env()

TEMP_DIR = pathlib.Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "file_storage"
    db_pass: str = "file_storage"
    db_base: str = "file_storage"
    db_echo: bool = False
    secret_key = env("SECRET_KEY")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app_dir = pathlib.Path(base_dir, "file_storage")
    template_dir = pathlib.Path(app_dir, "templates")
    static_dir = pathlib.Path(app_dir, "static")

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )


settings = Settings()
