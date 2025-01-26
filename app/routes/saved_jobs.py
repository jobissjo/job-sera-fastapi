from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.jobs import ResponseJobModel
from app.schema.saved_jobs import SavedJobSchema
from sqlalchemy.orm import Session
from app.schema.users import ResponseUser
from app.core.database import get_db
from sqlalchemy import MetaData
from app.utils.auth import get_current_active_user
from app.services import SavedJobService

router = APIRouter(prefix='/saved_jobs', tags=['Saved Jobs'])
metadata = MetaData()



@router.post('/', response_model=ResponseJobModel)
async def create_job(job_data:SavedJobSchema, db:Session = Depends(get_db), 
                     current_user:ResponseUser = Depends(get_current_active_user)):
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized for this request")

    return await SavedJobService.create_save_jobs(db,current_user.id,job_data)


@router.get('/user/{id}', response_model=list[ResponseJobModel])
async def get_jobs(id: str,db:Session= Depends(get_db),
                   current_user:ResponseUser = Depends(get_current_active_user)):
    jobs = await SavedJobService.get_user_saved_jobs(id, db)
    return jobs

@router.get('/{id}', response_model=ResponseJobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db),
                        current_user:ResponseUser = Depends(get_current_active_user)):
    
    filtered_job = await SavedJobService.get_saved_job(db,current_user.id, id)
    return filtered_job


@router.delete('/{id}')
async def delete_job(id:str, db:Session= Depends(get_db),
                      current_user:ResponseUser = Depends(get_current_active_user)):

    return await SavedJobService.delete_saved_job(db,current_user.id,id,)
