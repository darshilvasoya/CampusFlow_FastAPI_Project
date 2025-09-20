# routers/students.py

from fastapi import APIRouter, HTTPException, Depends # Added Depends
from db.database import get_db_cursor
from db.models import StudentCreate, User # Added User
from core.security import get_current_admin_user, get_current_admin_or_professor_user # Added role dependencies

student_router = APIRouter()

@student_router.post("/students", summary="Create a new student", tags=['Students'])
def create_student(user: StudentCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        # Note: The table is named `reg`. Consider renaming to `students` for clarity.
        with get_db_cursor(commit=True) as cursor:
            query = "INSERT INTO reg (name, age, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (user.name, user.age, user.email))
            return {"message": "Student created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create student: {e}")

@student_router.get("/students", summary="Get all students", tags=['Students'])
def get_all_students(current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id, name, age, email FROM reg")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@student_router.get("/students/{student_id}", summary="Get a single student by ID", tags=['Students'])
def get_student_by_id(student_id: int, current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id, name, age, email FROM reg WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
            return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@student_router.put("/students/{student_id}", summary="Update a student", tags=['Students'])
def update_student(student_id: int, user: StudentCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "UPDATE reg SET name = %s, age = %s, email = %s WHERE id = %s"
            cursor.execute(query, (user.name, user.age, user.email, student_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            return {"message": "Student updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update student: {e}")

@student_router.delete("/students/{student_id}", summary="Delete a student", tags=['Students'])
def delete_student(student_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "DELETE FROM reg WHERE id = %s"
            cursor.execute(query, (student_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
            return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete student: {e}")
