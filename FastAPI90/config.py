from pydantic import ValidationError
from pydantic.v1 import BaseSettings
import os



class Settings(BaseSettings):#pydantic will handle capitalization
    database_host : str
    database_port : int
    database_name:str
    database_username : str
    database_password: str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int


    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')


settings = Settings()


