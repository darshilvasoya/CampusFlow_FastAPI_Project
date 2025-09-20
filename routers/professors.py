# routers/professors.py

from fastapi import APIRouter, HTTPException, Depends # Added Depends
from db.database import get_db_cursor
from db.models import ProfessorCreate, User # Added User
from core.security import get_current_admin_user, get_current_active_user # Added role dependencies

professors_router = APIRouter()

@professors_router.post("/professors", summary="Create a new professor", tags=['Professors'])
def create_professor(professor: ProfessorCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "INSERT INTO professors (name, email, department_id, title) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (professor.name, professor.email, professor.department_id, professor.title))
            return {"message": "Professor created successfully"}
    except Exception as e:
        # Handle foreign key violation specifically
        if "1452" in str(e):
             raise HTTPException(status_code=400, detail=f"Failed to create professor: Department ID {professor.department_id} does not exist.")
        raise HTTPException(status_code=400, detail=f"Failed to create professor: {e}")

@professors_router.get("/professors", summary="Get all professors", tags=['Professors'])
def get_professors(current_user: User = Depends(get_current_active_user)): # Protected by any active user
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM professors")
            return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@professors_router.get("/professors/{professor_id}", summary="Get a single professor by ID", tags=['Professors'])
def get_professor_by_id(professor_id: int, current_user: User = Depends(get_current_active_user)): # Protected by any active user
    try:
        with get_db_cursor() as cursor:
            query = "SELECT * FROM professors WHERE id = %s"
            cursor.execute(query, (professor_id,))
            professor = cursor.fetchone()
            if not professor:
                raise HTTPException(status_code=404, detail="Professor not found")
            return professor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@professors_router.put("/professors/{professor_id}", summary="Update a professor", tags=['Professors'])
def update_professor(professor_id: int, professor: ProfessorCreate, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "UPDATE professors SET name = %s, email = %s, department_id = %s, title = %s WHERE id = %s"
            cursor.execute(query, (professor.name, professor.email, professor.department_id, professor.title, professor_id))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Professor not found")
            return {"message": "Professor updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update professor: {e}")

@professors_router.delete("/professors/{professor_id}", summary="Delete a professor", tags=['Professors'])
def delete_professor(professor_id: int, current_user: User = Depends(get_current_admin_user)): # Protected by admin
    try:
        with get_db_cursor(commit=True) as cursor:
            query = "DELETE FROM professors WHERE id = %s"
            cursor.execute(query, (professor_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Professor not found")
            return {"message": "Professor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete professor: {e}")