from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List
from uuid import UUID

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db=db, department=department)

@app.get("/departments/", response_model=List[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.get_departments(db, skip=skip, limit=limit)
    return departments

@app.get("/departments/{department_id}", response_model=schemas.Department)
def read_department(department_id: UUID, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@app.put("/departments/{department_id}", response_model=schemas.Department)
def update_department(department_id: UUID, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.update_department(db=db, department_id=department_id, department=department)

@app.delete("/departments/{department_id}")
def delete_department(department_id: UUID, db: Session = Depends(get_db)):
    db_department = crud.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    crud.delete_department(db=db, department_id=department_id)
    return {"detail": "Department deleted successfully"}
