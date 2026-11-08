from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id_str: Optional[str] = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.role or current_user.role.name != "system_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges",
        )
    return current_user


def check_facility_access(current_user: User, facility_id: int) -> bool:
    """Ensure user has right to query or mutate a specific facility."""
    if not current_user.role:
        return False
    # System admins and regional managers have cross-facility access
    if current_user.role.name in ["system_admin", "regional_supply_chain_manager", "data_analyst", "auditor"]:
        return True
    # Facility managers can only access their assigned facility
    if current_user.facility_id == facility_id:
        return True
    return False
