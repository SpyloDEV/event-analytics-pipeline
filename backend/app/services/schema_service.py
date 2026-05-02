from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.event import EventSchema
from app.repositories.analytics import AnalyticsRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import WRITE_ROLES, PermissionService


class SchemaService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> EventSchema:
        project = await self.repository.get_project_for_user(
            data["project_id"], user_id
        )
        if project is None:
            raise NotFoundError("Project not found.")
        await self.permissions.require_project_role(
            project_id=project.id, user_id=user_id, allowed_roles=WRITE_ROLES
        )
        schema = await self.repository.create_schema(data)
        await self.audit_logs.record(
            action="schema_created",
            organization_id=project.organization_id,
            project_id=project.id,
            actor_id=user_id,
            target_type="schema",
            target_id=schema.id,
        )
        return schema

    async def list(
        self, *, user_id: str, project_id: str | None = None
    ) -> list[EventSchema]:
        if project_id:
            project = await self.repository.get_project_for_user(project_id, user_id)
            if project is None:
                raise NotFoundError("Project not found.")
            return list(await self.repository.list_schemas(project_id=project_id))
        schemas: list[EventSchema] = []
        for project in await self.repository.list_projects(user_id=user_id):
            schemas.extend(await self.repository.list_schemas(project_id=project.id))
        return schemas

    async def get(self, *, schema_id: str, user_id: str) -> EventSchema:
        schema = await self.repository.get_schema_by_id(schema_id)
        if schema is None:
            raise NotFoundError("Schema not found.")
        if (
            await self.repository.get_project_for_user(schema.project_id, user_id)
            is None
        ):
            raise NotFoundError("Schema not found.")
        return schema

    async def update(self, *, schema_id: str, user_id: str, data: dict) -> EventSchema:
        schema = await self.get(schema_id=schema_id, user_id=user_id)
        await self.permissions.require_project_role(
            project_id=schema.project_id, user_id=user_id, allowed_roles=WRITE_ROLES
        )
        for key, value in data.items():
            if value is not None:
                setattr(schema, key, value)
        return schema
