from enum import Enum
from typing import List
from fastapi import HTTPException, status


class RoleEnum(str, Enum):
    SYSTEM_ADMIN = "system_admin"
    FACILITY_PHARMACY_MANAGER = "facility_pharmacy_manager"
    REGIONAL_SUPPLY_CHAIN_MANAGER = "regional_supply_chain_manager"
    DATA_ANALYST = "data_analyst"
    AUDITOR = "auditor"


class PermissionChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_role: str) -> bool:
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {self.allowed_roles}",
            )
        return True
