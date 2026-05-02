from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.enums import ProjectRole
from app.models.workspace import Organization, Project
from app.repositories.analytics import AnalyticsRepository
from app.services.audit_log_service import AuditLogService
from app.utils.slug import slugify


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, name: str) -> Organization:
        organization = await self.repository.create_organization(
            {"name": name, "slug": slugify(name), "created_by": user_id}
        )
        await self.audit_logs.record(
            action="organization_created",
            organization_id=organization.id,
            actor_id=user_id,
            target_type="organization",
            target_id=organization.id,
        )
        return organization

    async def list(self, *, user_id: str) -> list[Organization]:
        return list(await self.repository.list_organizations(user_id=user_id))


class ProjectService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> Project:
        organization = await self.repository.get_organization(data["organization_id"])
        if organization is None:
            raise NotFoundError("Organization not found.")
        if organization.created_by != user_id:
            raise PermissionDeniedError(
                "Only the organization owner can create projects."
            )
        project = await self.repository.create_project(data)
        await self.repository.create_project_member(
            {"project_id": project.id, "user_id": user_id, "role": ProjectRole.OWNER}
        )
        await self.audit_logs.record(
            action="project_created",
            organization_id=organization.id,
            project_id=project.id,
            actor_id=user_id,
            target_type="project",
            target_id=project.id,
        )
        return project

    async def get(self, *, project_id: str, user_id: str) -> Project:
        project = await self.repository.get_project_for_user(project_id, user_id)
        if project is None:
            raise NotFoundError("Project not found.")
        return project

    async def list(self, *, user_id: str) -> list[Project]:
        return list(await self.repository.list_projects(user_id=user_id))
