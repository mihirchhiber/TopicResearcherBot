from fastapi import FastAPI, Path

app = FastAPI()

dc = {}
dc[1] = "mihir"
dc[2] = "vishal"
dc["try"] = "vishal"

@app.get("/")
def index():
    return {"name": "Mihir"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description = "ID of the student you want to view")):
    return dc[student_id]

@app.get("/get")
def get_student(student_id: str = Path(..., description = "ID of the student you want to view")):
    print(student_id)
    return dc[student_id]
