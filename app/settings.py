from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    LOG_LEVEL: str = "INFO"
    LOG_FILE_NAME: str = "boge.log"
    LOG_MAX_FILE_SIZE_MB: int = 10
    LOG_FORMAT: str = "%(asctime)s:[%(levelname)s]:%(name)s:%(message)s"
    DEBUG: bool = False

    VERSION: str = "?"
    
