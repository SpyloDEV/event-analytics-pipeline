from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLogRead(BaseModel):
    id: str
    organization_id: str | None
    project_id: str | None
    actor_id: str | None
    action: str
    target_type: str | None
    target_id: str | None
    metadata_json: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}
