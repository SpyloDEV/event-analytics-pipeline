from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PermissionDeniedError
from app.models.enums import ProjectRole
from app.repositories.analytics import AnalyticsRepository

WRITE_ROLES = {ProjectRole.OWNER, ProjectRole.ADMIN, ProjectRole.DEVELOPER}
ANALYTICS_ROLES = {
    ProjectRole.OWNER,
    ProjectRole.ADMIN,
    ProjectRole.DEVELOPER,
    ProjectRole.ANALYST,
}
ADMIN_ROLES = {ProjectRole.OWNER, ProjectRole.ADMIN}


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def require_project_role(
        self,
        *,
        project_id: str,
        user_id: str,
        allowed_roles: Iterable[ProjectRole],
    ) -> ProjectRole:
        member = await self.repository.get_project_member(
            project_id=project_id,
            user_id=user_id,
        )
        if member is None or member.role not in set(allowed_roles):
            raise PermissionDeniedError("You do not have access to this project.")
        return member.role
