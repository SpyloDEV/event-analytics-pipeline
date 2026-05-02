from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.audit_log import AuditLog
from app.repositories.analytics import AnalyticsRepository


class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def record(
        self,
        *,
        action: str,
        organization_id: str | None = None,
        project_id: str | None = None,
        actor_id: str | None = None,
        target_type: str | None = None,
        target_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        return await self.repository.create_audit_log(
            data={
                "organization_id": organization_id,
                "project_id": project_id,
                "actor_id": actor_id,
                "action": action,
                "target_type": target_type,
                "target_id": target_id,
                "metadata_json": metadata or {},
            }
        )

    async def list_logs(
        self, *, user_id: str, project_id: str | None = None, limit: int = 100
    ) -> list[AuditLog]:
        if project_id is not None:
            project = await self.repository.get_project_for_user(project_id, user_id)
            if project is None:
                raise NotFoundError("Project not found.")
        return list(
            await self.repository.list_audit_logs(project_id=project_id, limit=limit)
        )
