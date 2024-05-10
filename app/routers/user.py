from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2, utils


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_a_user(user: schemas.UserCreate, db: Session=Depends(database.get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=schemas.UserResponse)
def get_a_user(db: Session=Depends(database.get_db), user_data: str=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==user_data.id).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'user not found!!')
    return user

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(db: Session=Depends(database.get_db), user_data: str=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==user_data.id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found!!')
    user.delete(synchronize_session=False)
    db.commit()
