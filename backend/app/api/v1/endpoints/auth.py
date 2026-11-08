from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService
from app.schemas.auth import Token, LoginRequest, LoginResponse, RefreshTokenRequest, UserSummary
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=Token, summary="OAuth2 standard login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login, getting an access token for future requests."""
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


@router.post("/login/json", response_model=LoginResponse, summary="JSON payload login")
def login_json(
    body: LoginRequest,
    db: Session = Depends(get_db)
):
    """Direct JSON body login for Single Page Applications (Next.js / React)."""
    service = AuthService(db)
    user = service.authenticate_user(body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    AuditService.log_action(db, "USER_LOGIN_JSON", "User", user_id=user.id, entity_id=str(user.id))
    token = service.create_user_token(user)
    user_summary = service.get_user_summary(user)
    return LoginResponse(token=token, user=user_summary)


@router.get("/me", response_model=UserSummary, summary="Get current logged in user details")
def read_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    return service.get_user_summary(current_user)


@router.post("/refresh", response_model=Token, summary="Refresh access token")
def refresh_token(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    new_token = service.refresh_token(body.token)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token for refresh",
        )
    return new_token


@router.post("/logout", summary="Logout current session")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    AuditService.log_action(db, "USER_LOGOUT", "User", user_id=current_user.id, entity_id=str(current_user.id))
    return {"message": "Successfully logged out"}
