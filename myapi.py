from fastapi import FastAPI, Path, HTTPException, Query, status
from typing import Optional, Dict, List
from pydantic import BaseModel

app = FastAPI(title="Student API", version="0.1")


# ---- Models ----

class StudentBase(BaseModel):
    name: str
    age: int
    year: str


class StudentCreate(StudentBase):
    pass


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


class Student(StudentBase):
    id: int


students: Dict[int, Student] = {
    1: Student(id=1, name="john", age=17, year="year 12")
}


def next_id() -> int:
    return max(students) + 1 if students else 1

# ---- Routes ----


@app.get("/", summary="Welcome")
def index():
    return {"message": "Welcome to my Student API"}


@app.get("/student/{student_id}", response_model=Student, summary="Get by ID")
def get_studnet(student_id: int =
                Path(..., description="The ID of the student yo want to view", gt=0)):
    try:
        return students[student_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail="Student not found!")


@app.get("/student", response_model=List[Student], summary="Filter by nameName")
def get_students_by_name(name: Optional[str] = Query(None, description="Filter by exact name (case-insensitive")):
    if name is None:
        return list(students.values())
    filtered = [s for s in students.values() if s.name.lower() == name.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="Student not found!")
    return filtered


@app.post("/student", response_model=Student, status_code=status.HTTP_201_CREATED, summary="Create Student")
def create_student(student: StudentCreate):
    sid = next_id()
    if sid in students:
        raise HTTPException(
            status_code=409, detail="Student already exists!")
    new_student = Student(id=sid, **student.model_dump())
    students[sid] = new_student
    return new_student


@app.patch("/student/{student_id}", response_model=Student, summary="Update (partial)")
def update_student(student_id: int, patch: UpdateStudent):
    current = students.get(student_id)
    if not current:
        raise HTTPException(status_code=404, detail="Student not found!")
    
    if patch.name is not None:
        current.name = patch.name
    if patch.age is not None:
        current.age = patch.age
    if patch.year is not None:
        current.year = patch.year

    students[student_id] = current
    return current


@app.delete("/student/{student_id}", response_model=Student, summary="Delete student")
def delete_student(student_id: int):
    deletedStudent = students.pop(student_id, None)
    if not deletedStudent:
        raise HTTPException(status_code=404, detail="Student not found!")        
    return deletedStudent
