
from fastapi import Depends,status,HTTPException
from jose import JWTError,jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from FastAPI import schemas, models, database
from fastapi.security import OAuth2PasswordBearer

from FastAPI.config import settings
from FastAPI.database import get_db

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

#Secret_Key
Secret_Key = settings.secret_key
#ALgorithm
Algorithm = settings.algorithm
#Experation_Time
Expiration_Time = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Expiration_Time)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,Secret_Key,algorithm = Algorithm)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,Secret_Key,algorithms = [Algorithm])
        user_id: str = payload.get("user_id") ##in the payload we passed it in as userdata when
        #we created the token
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(user_id)) #we create a pydantic model with the id that was passed in
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Could not validate credentials",headers = {"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

