from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):

    LOG_LEVEL: str = "INFO"
    LOG_FILE_NAME: str = "boge.log"
    LOG_MAX_FILE_SIZE_MB: int = 10
    LOG_FORMAT: str = "%(asctime)s:[%(levelname)s]:%(name)s:%(message)s"
    DEBUG: bool = False

    VERSION: str = "?"

    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_TOPIC: str
    MQTT_CLIENT_ID: str
    MQTT_USER: str
    MQTT_PASSWORD: SecretStr
