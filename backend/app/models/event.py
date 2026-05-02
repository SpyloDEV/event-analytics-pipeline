from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import (
    AnomalySeverity,
    AnomalyStatus,
    IngestionStatus,
    PipelineLogLevel,
    enum_values,
)


class RawEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "raw_events"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    event_name: Mapped[str] = mapped_column(String(180), index=True)
    user_id: Mapped[str | None] = mapped_column(String(180), index=True)
    anonymous_id: Mapped[str | None] = mapped_column(String(180), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    properties: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    context: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    ingestion_status: Mapped[IngestionStatus] = mapped_column(
        Enum(IngestionStatus, values_callable=enum_values, native_enum=False),
        default=IngestionStatus.ACCEPTED,
        nullable=False,
        index=True,
    )
    validation_errors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)


class EventSchema(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "event_schemas"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    event_name: Mapped[str] = mapped_column(String(180), index=True)
    required_properties: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
    optional_properties: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
    property_types: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class EventAggregate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "event_aggregates"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    metric_name: Mapped[str] = mapped_column(String(180), index=True)
    grain: Mapped[str] = mapped_column(String(40), default="day", nullable=False)
    bucket: Mapped[str] = mapped_column(String(80), index=True)
    value: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dimensions: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class Funnel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "funnels"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(180), index=True)
    steps: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Anomaly(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "anomalies"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(240), index=True)
    severity: Mapped[AnomalySeverity] = mapped_column(
        Enum(AnomalySeverity, values_callable=enum_values, native_enum=False),
        default=AnomalySeverity.MEDIUM,
        nullable=False,
        index=True,
    )
    status: Mapped[AnomalyStatus] = mapped_column(
        Enum(AnomalyStatus, values_callable=enum_values, native_enum=False),
        default=AnomalyStatus.OPEN,
        nullable=False,
        index=True,
    )
    signal: Mapped[str] = mapped_column(String(180), index=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)


class PipelineLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "pipeline_logs"

    project_id: Mapped[str] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        index=True,
    )
    raw_event_id: Mapped[str | None] = mapped_column(
        ForeignKey("raw_events.id", ondelete="SET NULL"),
        index=True,
    )
    level: Mapped[PipelineLogLevel] = mapped_column(
        Enum(PipelineLogLevel, values_callable=enum_values, native_enum=False),
        default=PipelineLogLevel.INFO,
        nullable=False,
        index=True,
    )
    message: Mapped[str] = mapped_column(Text)
    event_name: Mapped[str | None] = mapped_column(String(180), index=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
