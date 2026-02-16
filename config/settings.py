from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    BOT_TOKEN: str
    ADMIN_IDS: str = ""
    DATABASE_PATH: str = "data/bot.db"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_PERIOD: int = 60
    
    @property
    def admin_ids_list(self) -> list[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]
    
    @property
    def database_dir(self) -> Path:
        return Path(self.DATABASE_PATH).parent


settings = Settings()
