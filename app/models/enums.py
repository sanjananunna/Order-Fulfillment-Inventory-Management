from enum import Enum


class ActiveStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"