from enum import StrEnum


def enum_values(enum_cls):
    return [item.value for item in enum_cls]


class ProjectRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


class UserRole(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


class ApiKeyStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"


class IngestionStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PROCESSED = "processed"
    FAILED = "failed"


class PipelineLogLevel(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class AnomalySeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
