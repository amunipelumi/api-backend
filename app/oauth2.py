from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .config import settings
from . import schemas, database, models


oauth2_schema = OAuth2PasswordBearer('/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire_min


def access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token(token: str, exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username:str = payload.get('username')

        if not username:
            raise exception
        
        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise exception
    
    return token_data
    
def get_current_user(
        token: str=Depends(oauth2_schema), 
        db: Session=Depends(database.get_db)
        ):
    
    exception = HTTPException(status.HTTP_401_UNAUTHORIZED, 
                              'invalid credentials!!',
                              {'WWW-Authenticate': 'Bearer'})
    
    token_data = verify_token(token, exception)

    user = (db.query(models.User)
            .filter(models.User.username==token_data.username)
            .first())
    
    return user
