from enum import Enum
from typing import List, Union
from fastapi import HTTPException, status


class RoleEnum(str, Enum):
    ADMIN = "admin"
    SYSTEM_ADMIN = "system_admin"
    PHARMACY_MANAGER = "pharmacy_manager"
    FACILITY_PHARMACY_MANAGER = "facility_pharmacy_manager"
    REGIONAL_MANAGER = "regional_manager"
    REGIONAL_SUPPLY_CHAIN_MANAGER = "regional_supply_chain_manager"
    DATA_ANALYST = "data_analyst"
    AUDITOR = "auditor"


ROLE_ALIASES = {
    "admin": ["admin", "system_admin"],
    "system_admin": ["admin", "system_admin"],
    "pharmacy_manager": ["pharmacy_manager", "facility_pharmacy_manager"],
    "facility_pharmacy_manager": ["pharmacy_manager", "facility_pharmacy_manager"],
    "regional_manager": ["regional_manager", "regional_supply_chain_manager"],
    "regional_supply_chain_manager": ["regional_manager", "regional_supply_chain_manager"],
    "data_analyst": ["data_analyst"],
    "auditor": ["auditor"],
}


class PermissionChecker:
    """Dependency that checks if the user's role is in the allowed roles."""
    def __init__(self, allowed_roles: List[Union[str, RoleEnum]]):
        expanded = []
        for r in allowed_roles:
            val = r.value if isinstance(r, RoleEnum) else str(r)
            expanded.extend(ROLE_ALIASES.get(val, [val]))
        self.allowed_roles = set(expanded)

    def __call__(self, user_role: str) -> bool:
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {list(self.allowed_roles)}",
            )
        return True
