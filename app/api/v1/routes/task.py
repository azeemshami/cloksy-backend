from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate
from app.db.session import get_db
from app.repositories.task import TaskRepository


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_tasks(db: AsyncSession=Depends(get_db)):
    data = await TaskRepository.get_all(db)
    if not data:
        raise HTTPException(status_code=404, detail="No tasks found")
    return data

@router.get("/{task_id}")
async def get_task(task_id: int):
    if task_id < 1:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "message": "Task details"}


@router.post("/")
async def create_task(request: TaskCreate, db: AsyncSession=Depends(get_db)):
    task = await TaskRepository.create(request.model_dump(), db)
    if not task:
        raise HTTPException(status_code=400, detail="Task creation failed")
    return {"message": "Task created", "data": task}


@router.put("/{task_id}")
async def update_task(task_id: int, request: TaskCreate, db: AsyncSession=Depends(get_db)):
    task= await TaskRepository.get_by_id(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    payload = {
        **task.to_dict(),
        **request.model_dump(),
    }

    task = await TaskRepository.update(task_id, payload, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "message": "Task updated"}


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession=Depends(get_db)):
    deleted = await TaskRepository.delete(task_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"task_id": task_id, "message": "Task deleted"}
