from pydantic import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB__")

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str

    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class Settings:
    db_settings = DBSettings()


settings = Settings()
