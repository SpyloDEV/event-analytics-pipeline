from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.enums import IngestionStatus
from app.models.event import RawEvent
from app.repositories.analytics import AnalyticsRepository


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def list(
        self,
        *,
        project_id: str | None = None,
        failed_only: bool = False,
        limit: int = 100,
    ) -> list[RawEvent]:
        status = IngestionStatus.FAILED if failed_only else None
        return list(
            await self.repository.list_raw_events(
                project_id=project_id,
                status=status,
                limit=limit,
            )
        )

    async def get(self, *, event_id: str) -> RawEvent:
        event = await self.repository.get_raw_event(event_id)
        if event is None:
            raise NotFoundError("Event not found.")
        return event
