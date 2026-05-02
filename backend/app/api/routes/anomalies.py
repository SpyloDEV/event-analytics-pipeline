from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.event import AnomalyRead
from app.services.anomaly_service import AnomalyService

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


@router.get("", response_model=list[AnomalyRead])
async def list_anomalies(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[AnomalyRead]:
    return await AnomalyService(session).list(project_id=project_id)


@router.patch("/{anomaly_id}/resolve", response_model=AnomalyRead)
async def resolve_anomaly(
    anomaly_id: str,
    session: DbSession,
    _: CurrentUser,
) -> AnomalyRead:
    anomaly = await AnomalyService(session).resolve(anomaly_id=anomaly_id)
    await session.commit()
    await session.refresh(anomaly)
    return anomaly
