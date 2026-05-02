from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import ApiKey
from app.models.enums import IngestionStatus
from app.models.event import RawEvent
from app.repositories.analytics import AnalyticsRepository
from app.schemas.event import TrackEventRequest
from app.services.pipeline_log_service import PipelineLogService
from app.services.validation_service import ValidationService


class IngestionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.pipeline_logs = PipelineLogService(session)
        self.validation = ValidationService(session)

    async def track(self, *, api_key: ApiKey, payload: TrackEventRequest) -> RawEvent:
        event = await self.repository.create_raw_event(
            {
                "project_id": api_key.project_id,
                "event_name": payload.event_name,
                "user_id": payload.user_id,
                "anonymous_id": payload.anonymous_id,
                "timestamp": payload.timestamp or datetime.now(UTC),
                "properties": payload.properties,
                "context": payload.context,
                "ingestion_status": IngestionStatus.ACCEPTED,
                "validation_errors": [],
            }
        )
        await self.pipeline_logs.write(
            project_id=event.project_id,
            raw_event_id=event.id,
            event_name=event.event_name,
            message="event received",
        )
        return await self.validation.validate_event(event)

    async def batch(
        self, *, api_key: ApiKey, events: list[TrackEventRequest]
    ) -> list[RawEvent]:
        processed = []
        for payload in events:
            processed.append(await self.track(api_key=api_key, payload=payload))
        return processed
