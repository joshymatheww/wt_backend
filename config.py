from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")

    database_url: str
    origins: str

    admin_first_name: str
    admin_last_name: str
    admin_email: EmailStr
    admin_password: str

    jwt_secret_key: SecretStr
    algorithm: str
    access_token_expires: int = 30

    @property
    def get_cors_origins(self) -> list[str]:
        return self.origins.split(",")


settings = Settings()
