from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import IngestionStatus
from app.repositories.analytics import AnalyticsRepository


class AggregationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def top_events(self, *, project_id: str | None = None) -> list[dict]:
        events = await self.repository.list_raw_events(
            project_id=project_id, limit=1000
        )
        counts = Counter(event.event_name for event in events)
        return [
            {"event_name": event_name, "count": count}
            for event_name, count in counts.most_common(10)
        ]

    async def countries(self, *, project_id: str | None = None) -> list[dict]:
        events = await self.repository.list_raw_events(
            project_id=project_id, limit=1000
        )
        counts = Counter(event.context.get("country", "unknown") for event in events)
        return [{"country": key, "count": value} for key, value in counts.most_common()]

    async def sources(self, *, project_id: str | None = None) -> list[dict]:
        events = await self.repository.list_raw_events(
            project_id=project_id, limit=1000
        )
        counts = Counter(event.properties.get("source", "unknown") for event in events)
        return [{"source": key, "count": value} for key, value in counts.most_common()]

    async def error_rate(self, *, project_id: str | None = None) -> float:
        events = await self.repository.list_raw_events(
            project_id=project_id, limit=1000
        )
        if not events:
            return 0
        failed = sum(
            event.ingestion_status in {IngestionStatus.FAILED, IngestionStatus.REJECTED}
            for event in events
        )
        return round(failed / len(events) * 100, 2)
