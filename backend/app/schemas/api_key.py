from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ApiKeyStatus


class ApiKeyCreate(BaseModel):
    project_id: str
    name: str = Field(min_length=2, max_length=180)
    scopes: list[str] = Field(default_factory=lambda: ["events:write"])
    requests_per_minute: int = Field(default=1000, ge=1, le=100000)


class ApiKeyRead(BaseModel):
    id: str
    project_id: str
    name: str
    key_prefix: str
    scopes: list
    requests_per_minute: int
    status: ApiKeyStatus
    last_used_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ApiKeyCreated(ApiKeyRead):
    secret: str
