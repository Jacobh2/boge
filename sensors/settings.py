from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):

    LOG_LEVEL: str = "INFO"
    LOG_FILE_NAME: str = "boge.log"
    LOG_MAX_FILE_SIZE_MB: int = 10
    LOG_FORMAT: str = "%(asctime)s:[%(levelname)s]:%(name)s:%(message)s"
    DEBUG: bool = False

    SLEEP_TIME: int = 30

    VERSION: str = "?"

    DEVICE_ID: str = ""

    MOISTURE_INPUT: int = 1
    # Approx values for when in air and in water.
    # Low = The value when in water
    # High = The value when dry in air
    MOISTURE_HIGH: float = 4.966
    MOISTURE_LOW: float = 2.0
    MOISTURE_ROUND: int = 10

    MQTT_BROKER: str
    MQTT_PORT: int
    MQTT_TOPIC: str
    MQTT_CLIENT_ID: str
    MQTT_USER: str
    MQTT_PASSWORD: SecretStr
