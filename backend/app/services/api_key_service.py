from datetime import UTC, datetime
from hashlib import sha256

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, NotFoundError
from app.core.security import generate_api_key
from app.models.api_key import ApiKey
from app.models.enums import ApiKeyStatus
from app.repositories.analytics import AnalyticsRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import ADMIN_ROLES, PermissionService


def hash_api_key(secret: str) -> str:
    return sha256(secret.encode()).hexdigest()


class ApiKeyService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> tuple[ApiKey, str]:
        project = await self.repository.get_project_for_user(
            data["project_id"], user_id
        )
        if project is None:
            raise NotFoundError("Project not found.")
        await self.permissions.require_project_role(
            project_id=project.id, user_id=user_id, allowed_roles=ADMIN_ROLES
        )
        secret = generate_api_key()
        api_key = await self.repository.create_api_key(
            {
                **data,
                "key_hash": hash_api_key(secret),
                "key_prefix": secret[:12],
                "status": ApiKeyStatus.ACTIVE,
            }
        )
        await self.audit_logs.record(
            action="api_key_created",
            organization_id=project.organization_id,
            project_id=project.id,
            actor_id=user_id,
            target_type="api_key",
            target_id=api_key.id,
        )
        return api_key, secret

    async def list(
        self, *, user_id: str, project_id: str | None = None
    ) -> list[ApiKey]:
        if project_id:
            await self.permissions.require_project_role(
                project_id=project_id,
                user_id=user_id,
                allowed_roles=ADMIN_ROLES,
            )
            return list(await self.repository.list_api_keys(project_id=project_id))
        keys: list[ApiKey] = []
        for project in await self.repository.list_projects(user_id=user_id):
            keys.extend(await self.repository.list_api_keys(project_id=project.id))
        return keys

    async def revoke(self, *, api_key_id: str, user_id: str) -> ApiKey:
        api_key = await self.repository.get_api_key(api_key_id)
        if api_key is None:
            raise NotFoundError("API key not found.")
        project = await self.repository.get_project_for_user(
            api_key.project_id, user_id
        )
        if project is None:
            raise NotFoundError("API key not found.")
        await self.permissions.require_project_role(
            project_id=project.id, user_id=user_id, allowed_roles=ADMIN_ROLES
        )
        api_key.status = ApiKeyStatus.REVOKED
        api_key.revoked_at = datetime.now(UTC)
        await self.audit_logs.record(
            action="api_key_revoked",
            organization_id=project.organization_id,
            project_id=project.id,
            actor_id=user_id,
            target_type="api_key",
            target_id=api_key.id,
        )
        return api_key

    async def authenticate(self, secret: str) -> ApiKey:
        api_key = await self.repository.get_api_key_by_hash(hash_api_key(secret))
        if api_key is None:
            raise AuthenticationError("Invalid or revoked API key.")
        api_key.last_used_at = datetime.now(UTC)
        return api_key
