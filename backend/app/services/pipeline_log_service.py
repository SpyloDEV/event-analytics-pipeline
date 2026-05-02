from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import PipelineLogLevel
from app.models.event import PipelineLog
from app.repositories.analytics import AnalyticsRepository


class PipelineLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def write(
        self,
        *,
        project_id: str,
        message: str,
        level: PipelineLogLevel = PipelineLogLevel.INFO,
        raw_event_id: str | None = None,
        event_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PipelineLog:
        return await self.repository.create_pipeline_log(
            {
                "project_id": project_id,
                "raw_event_id": raw_event_id,
                "level": level,
                "message": message,
                "event_name": event_name,
                "metadata_json": metadata or {},
            }
        )

    async def list(
        self, *, project_id: str | None = None, limit: int = 100
    ) -> list[PipelineLog]:
        return list(
            await self.repository.list_pipeline_logs(project_id=project_id, limit=limit)
        )
