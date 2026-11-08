from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserResponse
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    AuditService.log_action(db, "USER_LOGIN", "User", user_id=user.id, entity_id=str(user.id))
    return service.create_user_token(user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
