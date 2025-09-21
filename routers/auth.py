
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from core.security import create_access_token, verify_password, get_password_hash, get_current_admin_user
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from db.database import get_db_cursor
from db.models import Token, User, UserInDB

auth_router = APIRouter(tags=["Authentication"])


def get_user(db_cursor, username: str) -> UserInDB:
    """Helper function to get a user from the database."""
    query = "SELECT * FROM users WHERE username = %s"
    db_cursor.execute(query, (username,))
    user_data = db_cursor.fetchone()
    if user_data:
        return UserInDB(**user_data)
    return None


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db_cursor() as cursor:
        user = get_user(cursor, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None

@auth_router.post("/register", summary="Register a new user (default role: student)")
def register_user(user: UserRegister):
    with get_db_cursor(commit=True) as cursor:
        hashed_password = get_password_hash(user.password)
        query = "INSERT INTO users (username, hashed_password, email, full_name, role) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (user.username, hashed_password, user.email, user.full_name, "student"))
            return {"message": f"User '{user.username}' registered successfully with role 'student'."}
        except Exception as e:
            if "Duplicate entry" in str(e) and "for key 'username'" in str(e):
                raise HTTPException(status_code=400, detail="Username already exists.")
            raise HTTPException(status_code=400, detail=f"Failed to register user: {e}")


class UserRoleUpdate(BaseModel):
    role: str

@auth_router.put("/users/{username}/role", summary="Update a user's role (Admin only)")
def update_user_role(username: str, role_update: UserRoleUpdate, current_user: User = Depends(get_current_admin_user)):
    valid_roles = ["admin", "student", "professor"]
    if role_update.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
    with get_db_cursor(commit=True) as cursor:
        query = "UPDATE users SET role = %s WHERE username = %s"
        cursor.execute(query, (role_update.role, username))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        return {"message": f"User '{username}' role updated to '{role_update.role}'."}
