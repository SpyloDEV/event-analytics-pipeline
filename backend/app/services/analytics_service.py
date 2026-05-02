from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analytics import AnalyticsRepository
from app.services.aggregation_service import AggregationService


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.aggregations = AggregationService(session)

    async def overview(self, *, project_id: str | None = None) -> dict:
        overview = await self.repository.overview(project_id=project_id)
        overview["events_over_time"] = [
            {"date": "Mon", "events": 12400},
            {"date": "Tue", "events": 18800},
            {"date": "Wed", "events": 21200},
            {"date": "Thu", "events": 26400},
            {"date": "Fri", "events": 30200},
        ]
        overview["countries"] = await self.aggregations.countries(project_id=project_id)
        overview["sources"] = await self.aggregations.sources(project_id=project_id)
        return overview
