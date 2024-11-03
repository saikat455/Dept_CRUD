from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

students = {
    1: {
        "name": "John Doe",
        "age": 25,
        "year": 12
    },
    2: {
        "name": "John ",
        "age": 5, 
        "year": 1
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    return{"name": "First Data"}  

@app.get("/get-student/{student_id}")
def get_student(student_id:int = Path(description="The ID of the student you want to view", gt=0, lt=10)):
    return students[student_id] 

@app.get("/get-by-name/{student_id}")
def get_student_by_name(student_id: int, name: Optional[str] = None):
    if student_id not in students:
        return {"Data": "Student ID not found"}

    if name is None or students[student_id]["name"] == name:
        return students[student_id]

    return {"Data": "Name does not match the provided student ID"}

    

@app.post("/create-student/{student_id}")
def create_student(student_id : int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students[student_id]


@app.put("/update_student/{student_id}")
def update_student(student_id : int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student not found"}
    
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.year is not None:
        students[student_id]["year"] = student.year
     
    
    return students[student_id] 


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    # Check if the student_id exists in the dictionary
    if student_id not in students:
        return {"Error": "Student not found"}
    
    # Delete the student from the dictionary
    del students[student_id]
    return {"Message": f"Student with ID {student_id} has been deleted"}
