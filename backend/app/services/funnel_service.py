from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.event import Funnel
from app.repositories.analytics import AnalyticsRepository
from app.services.permissions import WRITE_ROLES, PermissionService


class FunnelService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.permissions = PermissionService(session)

    async def create(self, *, user_id: str, data: dict) -> Funnel:
        project = await self.repository.get_project_for_user(
            data["project_id"], user_id
        )
        if project is None:
            raise NotFoundError("Project not found.")
        await self.permissions.require_project_role(
            project_id=project.id, user_id=user_id, allowed_roles=WRITE_ROLES
        )
        return await self.repository.create_funnel(data)

    async def list(
        self, *, user_id: str, project_id: str | None = None
    ) -> list[Funnel]:
        if project_id:
            await self.permissions.require_project_role(
                project_id=project_id, user_id=user_id, allowed_roles=WRITE_ROLES
            )
            return list(await self.repository.list_funnels(project_id=project_id))
        funnels: list[Funnel] = []
        for project in await self.repository.list_projects(user_id=user_id):
            funnels.extend(await self.repository.list_funnels(project_id=project.id))
        return funnels

    async def results(self, *, funnel_id: str, user_id: str) -> dict:
        funnel = await self.repository.get_funnel(funnel_id)
        if funnel is None:
            raise NotFoundError("Funnel not found.")
        if (
            await self.repository.get_project_for_user(funnel.project_id, user_id)
            is None
        ):
            raise NotFoundError("Funnel not found.")
        events = await self.repository.list_raw_events(
            project_id=funnel.project_id, limit=5000
        )
        counts = Counter(event.event_name for event in events)
        first_count = max(counts.get(funnel.steps[0], 0), 1)
        steps = []
        for step in funnel.steps:
            count = counts.get(step, 0)
            steps.append(
                {
                    "event_name": step,
                    "count": count,
                    "conversion_rate": round(count / first_count * 100, 2),
                }
            )
        final_count = steps[-1]["count"] if steps else 0
        return {
            "funnel_id": funnel.id,
            "steps": steps,
            "overall_conversion_rate": round(final_count / first_count * 100, 2),
        }
