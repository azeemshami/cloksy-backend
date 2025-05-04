from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.db.session import get_db

class TaskRepository:

    async def get_all(db: AsyncSession=Depends(get_db)):
        data = await db.execute(select(Task))
        return data.scalars().all()

    async def get_by_id(task_id, db: AsyncSession=Depends(get_db)):
        data = await db.execute(select(Task).where(Task.id == task_id))
        return data.scalars().first()

    async def create(task_data, db: AsyncSession=Depends(get_db)):
        new_task = Task(**task_data)
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task
        

    async def update(task_id, task_data, db: AsyncSession=Depends(get_db)):
        await db.execute(update(Task).where(Task.id == task_id).values(**task_data))
        await db.commit()
        return True

    async def delete(task_id, db: AsyncSession=Depends(get_db)):
        await db.execute(delete(Task).where(Task.id == task_id))
        await db.commit()
        return True
        
