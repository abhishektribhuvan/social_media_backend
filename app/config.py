from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    database_password: str
    database_username: str
    database_port: int
    database_hostname: str
    secret_key: str
    database: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()
