from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

students = {
    1: {
        "name": "john",
        "age": 17,
        "class": "year 12"
    }
}


@app.get("/")
def index():
    return {
        "name": "First Data"
    }


@app.get("/get_student/{student_id}")
def get_studnet(student_id: int =
                Path(...,
                     description="The ID of the student yo want to view",
                     gt=0
                     )):    
    try:
        return students[student_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Student not found")
    
