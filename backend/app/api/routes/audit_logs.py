from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.audit_log import AuditLogRead
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("", response_model=list[AuditLogRead])
async def list_audit_logs(
    session: DbSession,
    user: CurrentUser,
    project_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[AuditLogRead]:
    return await AuditLogService(session).list_logs(
        user_id=user.id,
        project_id=project_id,
        limit=limit,
    )
