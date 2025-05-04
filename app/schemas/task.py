from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    name: str = Field(title="Task Title", example="Task Title")
    description: Optional[str] = Field(None, example="Task Description")
    estimated_time: Optional[str] = Field("Estimated Time", example="12h")
    spent_time: Optional[str] = Field(title="Spent Time", example="1h")
    status: Optional[str] = Field("pending", example="pending")

    class Config:
        orm_mode = True
class TaskCreate(TaskBase):
    pass
