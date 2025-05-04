from sqlalchemy import Column, Integer, String
from app.db.base import Base
from .timestamp import TimestampMixin

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    estimated_time = Column(String)  # 0 for false, 1 for true
    spent_time = Column(String)  # 0 for false, 1 for true
    status = Column(String, default="todo")  # 0 for false, 1 for true

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
