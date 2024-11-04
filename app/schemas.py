from pydantic import BaseModel
from uuid import UUID

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: UUID  # Change `str` to `UUID` here

    class Config:
        orm_mode = True
