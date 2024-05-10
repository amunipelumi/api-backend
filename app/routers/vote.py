from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database


router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def votes(
    vote: schemas.VotesInput, 
    db: Session=Depends(database.get_db), 
    user_data: str=Depends(oauth2.get_current_user)
    ):

    query = db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if not query:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {vote.post_id} does not exist!')

    vote_query = (
        db.query(models.Vote)
        .filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==user_data.id)
        )
    
    vote_found = vote_query.first()

    if vote.vote == 1:
        if vote_found:
            raise HTTPException(status.HTTP_409_CONFLICT, detail='voted already!')
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=user_data.id)
        db.add(new_vote)
        db.commit()

        return {'message': 'successfully added vote'}

    else:
        if not vote_found:
            raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail='you have no vote')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'successfully deleted vote'}
    