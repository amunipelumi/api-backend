from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm as oprf
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(
    user: oprf=Depends(), 
    db: Session=Depends(database.get_db)
    ):

    db_query = (db.query(models.User)
                .filter(models.User.username==user.username)
                .first())
    
    if not db_query:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    
    if not utils.verify(user.password, db_query.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    
    access_token = oauth2.access_token(data={'username': user.username})
    
    return {'access_token': access_token, 'token_type': 'bearer'}