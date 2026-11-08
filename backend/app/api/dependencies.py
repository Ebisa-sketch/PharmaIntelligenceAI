from typing import Callable, List, Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.permissions import RoleEnum, ROLE_ALIASES
from app.database.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)


def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

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
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account"
        )
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def require_roles(allowed_roles: List[Union[str, RoleEnum]]) -> Callable:
    """Dependency factory that ensures user has at least one of the allowed roles."""
    expanded: List[str] = []
    for r in allowed_roles:
        val = r.value if isinstance(r, RoleEnum) else str(r)
        expanded.extend(ROLE_ALIASES.get(val, [val]))
    allowed_set = set(expanded)

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role.name if current_user.role else ""
        if user_role not in allowed_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required role: {list(allowed_set)}",
            )
        return current_user

    return role_checker


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    user_role = current_user.role.name if current_user.role else ""
    if user_role not in ["admin", "system_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have administrative privileges",
        )
    return current_user


def check_facility_access(current_user: User, facility_id: int) -> bool:
    """Ensure user has authorization to view or mutate a facility's data."""
    if not current_user.role:
        return False
    user_role = current_user.role.name
    # System admins, regional managers, data analysts, and auditors have multi-facility access
    cross_facility_roles = ["admin", "system_admin", "regional_manager", "regional_supply_chain_manager", "data_analyst", "auditor"]
    if user_role in cross_facility_roles:
        return True
    # Facility managers can only access their explicitly assigned facility
    if current_user.facility_id == facility_id:
        return True
    return False
