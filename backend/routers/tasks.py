from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models
from ..schemas import Task,TaskResponse
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/",response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    ).all()


@router.get("/{task_id}",response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.post("/",response_model=TaskResponse)
def create_task(
    task: Task,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_task = models.Task(
        title=task.title,
        completed=task.completed,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{task_id}",response_model=TaskResponse)
def update_task(
    task_id: int,
    task: Task,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    existing_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    existing_task.title = task.title
    existing_task.completed = task.completed

    db.commit()
    db.refresh(existing_task)

    return existing_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    removing_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if removing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(removing_task)
    db.commit()

    return {"message": "successfully deleted the task"}


