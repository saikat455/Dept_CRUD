from sqlalchemy.orm import Session
from app import models, schemas

def get_department(db: Session, department_id: str):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(name=department.name)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def update_department(db: Session, department_id: str, department: schemas.DepartmentCreate):
    db_department = get_department(db, department_id)
    db_department.name = department.name
    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: str):
    db_department = get_department(db, department_id)
    db.delete(db_department)
    db.commit()
