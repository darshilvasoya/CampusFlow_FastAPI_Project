
from fastapi import FastAPI, Depends
from core.security import get_current_user


from routers.auth import auth_router
from routers.students import student_router
from routers.courses import course_router
from routers.departments import departments_router
from routers.enrollments import enrollments_router
from routers.professors import professors_router

app = FastAPI(
    title="CampusFlow API",
    description="The backend for the College Management System.",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(student_router, dependencies=[Depends(get_current_user)])
app.include_router(course_router, dependencies=[Depends(get_current_user)])
app.include_router(departments_router, dependencies=[Depends(get_current_user)])
app.include_router(enrollments_router, dependencies=[Depends(get_current_user)])
app.include_router(professors_router, dependencies=[Depends(get_current_user)])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the CampusFlow API! To see the documentation, add /docs to the current URL or visit https://campusflow-4n9z.onrender.com/docs."}
    
