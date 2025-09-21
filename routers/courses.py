from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db_cursor
from db.models import CourseCreate, User
from core.security import get_current_admin_user, get_current_active_user, get_current_professor_user

course_router = APIRouter()

@course_router.post("/courses", summary="Create a new course", tags=['Courses'])
def create_course(course: CourseCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "INSERT INTO courses (title, code, description, credits, department_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (course.title, course.code, course.description, course.credits, course.department_id))
            return {"message": "Course created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create course: {e}")

@course_router.get("/courses", summary="Get all courses", tags=['Courses'])
def get_all_courses(current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM courses")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@course_router.get("/courses/{course_id}", summary="Get a single course by ID", tags=['Courses'])
def get_course_by_id(course_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor() as cursor:
            query = "SELECT * FROM courses WHERE id = %s"
            cursor.execute(query, (course_id,))
            course = cursor.fetchone()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@course_router.put("/courses/{course_id}", summary="Update a course", tags=['Courses'])
def update_course(course_id: int, course: CourseCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "UPDATE courses SET title = %s, code = %s, description = %s, credits = %s, department_id = %s WHERE id = %s"
            cursor.execute(query, (course.title, course.code, course.description, course.credits, course.department_id, course_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Course not found")
            return {"message": "Course updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update course: {e}")

@course_router.delete("/courses/{course_id}", summary="Delete a course", tags=['Courses'])
def delete_course(course_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "DELETE FROM courses WHERE id = %s"
            cursor.execute(query, (course_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Course not found")
            return {"message": "Course deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete course: {e}")
