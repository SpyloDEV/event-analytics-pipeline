from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ProjectRole


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)


class OrganizationRead(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    organization_id: str
    name: str = Field(min_length=2, max_length=180)
    key: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9_-]+$")
    description: str | None = Field(default=None, max_length=500)


class ProjectRead(BaseModel):
    id: str
    organization_id: str
    name: str
    key: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectMemberRead(BaseModel):
    id: str
    project_id: str
    user_id: str
    role: ProjectRole
    created_at: datetime

    model_config = {"from_attributes": True}
