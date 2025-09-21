from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db_cursor
from db.models import Student, StudentCreate

student_router = APIRouter(prefix="/students", tags=["Students"])


@student_router.get("/", response_model=list[Student])
def get_all_students():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, name, age, email FROM students")
        students = [Student(**row) for row in cursor.fetchall()]
    return students


@student_router.get("/{student_id}", response_model=Student)
def get_student_by_id(student_id: int):
    with get_db_cursor() as cursor:
        try:
            cursor.execute("SELECT id, name, age, email FROM students WHERE id = %s", (student_id,))
            student_data = cursor.fetchone()
            if not student_data:
                raise HTTPException(status_code=404, detail="Student not found")
            return Student(**student_data)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@student_router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    with get_db_cursor(commit=True) as cursor:
        try:
            query = "INSERT INTO students (name, age, email) VALUES (%s, %s, %s) RETURNING id"
            cursor.execute(query, (student.name, student.age, student.email))
            new_student_id = cursor.fetchone()['id']
            return Student(id=new_student_id, **student.dict())
        except Exception as e:
            if "violates unique constraint" in str(e):
                raise HTTPException(status_code=400, detail="Email already exists.")
            raise HTTPException(status_code=500, detail=f"Failed to create student: {e}")


@student_router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate):
    with get_db_cursor(commit=True) as cursor:
        try:
            query = """
                UPDATE students
                SET name = %s, age = %s, email = %s
                WHERE id = %s
            """
            cursor.execute(query, (student.name, student.age, student.email, student_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            
            cursor.execute("SELECT id, name, age, email FROM students WHERE id = %s", (student_id,))
            updated_student_data = cursor.fetchone()
            return Student(**updated_student_data)
        except Exception as e:
            if "violates unique constraint" in str(e):
                raise HTTPException(status_code=400, detail="Email already exists for another student.")
            raise HTTPException(status_code=500, detail=f"Failed to update student: {e}")


@student_router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    with get_db_cursor(commit=True) as cursor:
        try:
            query = "DELETE FROM students WHERE id = %s"
            cursor.execute(query, (student_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete student: {e}")
