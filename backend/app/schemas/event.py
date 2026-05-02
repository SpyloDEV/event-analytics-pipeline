from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import (
    AnomalySeverity,
    AnomalyStatus,
    IngestionStatus,
    PipelineLogLevel,
)


class TrackEventRequest(BaseModel):
    event_name: str = Field(min_length=2, max_length=180)
    user_id: str | None = Field(default=None, max_length=180)
    anonymous_id: str | None = Field(default=None, max_length=180)
    timestamp: datetime | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)


class TrackEventResponse(BaseModel):
    event_id: str
    status: IngestionStatus


class BatchEventRequest(BaseModel):
    events: list[TrackEventRequest] = Field(min_length=1, max_length=500)


class BatchEventResponse(BaseModel):
    accepted_count: int
    event_ids: list[str]


class RawEventRead(BaseModel):
    id: str
    project_id: str
    event_name: str
    user_id: str | None
    anonymous_id: str | None
    timestamp: datetime
    properties: dict[str, Any]
    context: dict[str, Any]
    ingestion_status: IngestionStatus
    validation_errors: list
    created_at: datetime

    model_config = {"from_attributes": True}


class EventSchemaCreate(BaseModel):
    project_id: str
    event_name: str = Field(min_length=2, max_length=180)
    required_properties: dict[str, str] = Field(default_factory=dict)
    optional_properties: dict[str, str] = Field(default_factory=dict)
    property_types: dict[str, str] = Field(default_factory=dict)
    is_active: bool = True


class EventSchemaUpdate(BaseModel):
    required_properties: dict[str, str] | None = None
    optional_properties: dict[str, str] | None = None
    property_types: dict[str, str] | None = None
    is_active: bool | None = None


class EventSchemaRead(BaseModel):
    id: str
    project_id: str
    event_name: str
    required_properties: dict[str, str]
    optional_properties: dict[str, str]
    property_types: dict[str, str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FunnelCreate(BaseModel):
    project_id: str
    name: str = Field(min_length=2, max_length=180)
    steps: list[str] = Field(min_length=2, max_length=20)


class FunnelRead(BaseModel):
    id: str
    project_id: str
    name: str
    steps: list
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class FunnelResult(BaseModel):
    funnel_id: str
    steps: list[dict[str, Any]]
    overall_conversion_rate: float


class AnomalyRead(BaseModel):
    id: str
    project_id: str
    title: str
    severity: AnomalySeverity
    status: AnomalyStatus
    signal: str
    metadata_json: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}


class PipelineLogRead(BaseModel):
    id: str
    project_id: str
    raw_event_id: str | None
    level: PipelineLogLevel
    message: str
    event_name: str | None
    metadata_json: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}
