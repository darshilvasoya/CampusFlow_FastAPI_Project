# routers/enrollments.py

from fastapi import APIRouter, HTTPException, Depends # Added Depends
from db.database import get_db_cursor
from db.models import EnrollmentCreate, User # Added User
from core.security import get_current_admin_user, get_current_active_user, get_current_professor_user, get_current_admin_or_professor_user # Added role dependencies

enrollments_router = APIRouter()

@enrollments_router.post("/enrollments", summary="Create a new enrollment", tags=['Enrollments'])
def create_enrollment(enrollment: EnrollmentCreate, current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date, enrollment.grade))
            return {"message": "Enrollment created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create enrollment: {e}")

@enrollments_router.get("/enrollments", summary="Get all enrollments", tags=['Enrollments'])
def get_enrollments(current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM enrollments")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@enrollments_router.get("/enrollments/{enrollment_id}", summary="Get a single enrollment by ID", tags=['Enrollments'])
def get_enrollment_by_id(enrollment_id: int, current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor() as cursor:
            query = "SELECT * FROM enrollments WHERE id = %s"
            cursor.execute(query, (enrollment_id,))
            enrollment = cursor.fetchone()
            if not enrollment:
                raise HTTPException(status_code=404, detail="Enrollment not found")
            return enrollment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@enrollments_router.put("/enrollments/{enrollment_id}", summary="Update an enrollment", tags=['Enrollments'])
def update_enrollment(enrollment_id: int, enrollment: EnrollmentCreate, current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "UPDATE enrollments SET student_id = %s, course_id = %s, enrollment_date = %s, grade = %s WHERE id = %s"
            cursor.execute(query, (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date, enrollment.grade, enrollment_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Enrollment not found")
            return {"message": "Enrollment updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update enrollment: {e}")

@enrollments_router.delete("/enrollments/{enrollment_id}", summary="Delete an enrollment", tags=['Enrollments'])
def delete_enrollment(enrollment_id: int, current_user: User = Depends(get_current_admin_or_professor_user)): # Protected by admin or professor
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "DELETE FROM enrollments WHERE id = %s"
            cursor.execute(query, (enrollment_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Enrollment not found")
            return {"message": "Enrollment deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete enrollment: {e}")