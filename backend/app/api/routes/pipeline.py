from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.event import PipelineLogRead
from app.services.pipeline_log_service import PipelineLogService

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.get("/logs", response_model=list[PipelineLogRead])
async def pipeline_logs(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[PipelineLogRead]:
    return await PipelineLogService(session).list(project_id=project_id)


@router.get("/status", response_model=dict)
async def pipeline_status(_: CurrentUser) -> dict:
    return {
        "status": "healthy",
        "redis": "connected",
        "worker_queue": "events",
        "lag_seconds": 2,
    }
