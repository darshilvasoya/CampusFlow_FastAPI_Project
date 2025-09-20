# routers/departments.py

from fastapi import APIRouter, HTTPException, Depends # Added Depends
from db.database import get_db_cursor
from db.models import DepartmentCreate, User # Added User
from core.security import get_current_admin_user, get_current_active_user # Added role dependencies

departments_router = APIRouter()

@departments_router.post("/departments", summary="Create a new department", tags=['Departments'])
def create_department(department: DepartmentCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "INSERT INTO departments (name, code) VALUES (%s, %s)"
            cursor.execute(query, (department.name, department.code))
            return {"message": "Department created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create department: {e}")

@departments_router.get("/departments", summary="Get all departments", tags=['Departments'])
def get_departments(current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM departments")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@departments_router.get("/departments/{department_id}", summary="Get a single department by ID", tags=['Departments'])
def get_department_by_id(department_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor() as cursor:
            query = "SELECT * FROM departments WHERE id = %s"
            cursor.execute(query, (department_id,))
            department = cursor.fetchone()
            if not department:
                raise HTTPException(status_code=404, detail="Department not found")
            return department
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@departments_router.put("/departments/{department_id}", summary="Update a department", tags=['Departments'])
def update_department(department_id: int, department: DepartmentCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "UPDATE departments SET name = %s, code = %s WHERE id = %s"
            cursor.execute(query, (department.name, department.code, department_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Department not found")
            return {"message": "Department updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update department: {e}")

@departments_router.delete("/departments/{department_id}", summary="Delete a department", tags=['Departments'])
def delete_department(department_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "DELETE FROM departments WHERE id = %s"
            cursor.execute(query, (department_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Department not found")
            return {"message": "Department deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete department: {e}")
