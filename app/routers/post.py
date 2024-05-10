from typing import List, Optional
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

### Notes
# You make your sql queries, get back response and see the fields your query returns
# Then you define a response model schema that allows for a well defined output
###

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_a_post(
    post: schemas.PostCreate, 
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user)
    ):

    post.user_id = user_data.id
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print('ID:', user_data.id)
    print('USERNAME:', user_data.username)
    print('EMAIL:', user_data.email)
    print('ACTION: Created a post')

    return new_post

@router.get('/', response_model=List[schemas.PostResponse2])
def get_all_posts(
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user), 
    search: Optional[str]="", limit: int=10, skip: int=0
    ):
    
    # owner_all = (db.query(models.Post)
    #              .filter(models.Post.user_id==user_data.id, 
    #                      models.Post.title.contains(search))
    #              .limit(limit).offset(skip).all())

    owner_all = (db.query(models.Post, func.count(models.Vote.post_id).label("Votes"))
                .join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True)
                .group_by(models.Post.id)
                .filter(models.Post.title.contains(search))
                .limit(limit)
                .offset(skip)
                .all())
    
    print('ID:', user_data.id)
    print('USERNAME:', user_data.username)
    print('EMAIL:', user_data.email)
    print('ACTION: Searched all user posts')

    return owner_all

@router.get('/{id}', response_model=schemas.PostResponse)
def get_a_post(
    id: int, 
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user)
    ):

    single_post = (db.query(models.Post)
                   .filter(models.Post.id==id, models.Post.user_id==user_data.id)
                   .first())
    
    if not single_post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f'record not found!!')
    
    print('ID:', user_data.id)
    print('USERNAME:', user_data.username)
    print('EMAIL:', user_data.email)
    print('ACTION: Searched a user post')

    return single_post

@router.put('/{id}', response_model=schemas.PostResponse)
def update_a_post(
    id: int, 
    post: schemas.PostCreate, 
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user)
    ):

    query = (db.query(models.Post)
             .filter(models.Post.id==id, models.Post.user_id==user_data.id))
    u_post = query.first()

    if u_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found!!')
    
    post.user_id = user_data.id
    query.update(post.model_dump(), synchronize_session=False)
    db.commit() 

    print('ID:', user_data.id)
    print('USERNAME:', user_data.username)
    print('EMAIL:', user_data.email)
    print('ACTION: Updated a post')

    return query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(
    id: int, 
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user)
    ):
    
    post = (db.query(models.Post)
            .filter(models.Post.id==id, models.Post.user_id==user_data.id))

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found!!')
    
    post.delete(synchronize_session=False)
    db.commit()

    print('ID:', user_data.id)
    print('USERNAME:', user_data.username)
    print('EMAIL:', user_data.email)
    print('ACTION: Deleted a post')
    # return {'message': 'post deleted successfully'}
