from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.event import FunnelCreate, FunnelRead, FunnelResult
from app.services.funnel_service import FunnelService

router = APIRouter(prefix="/funnels", tags=["Funnels"])


@router.post("", response_model=FunnelRead, status_code=status.HTTP_201_CREATED)
async def create_funnel(
    payload: FunnelCreate,
    session: DbSession,
    user: CurrentUser,
) -> FunnelRead:
    funnel = await FunnelService(session).create(
        user_id=user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(funnel)
    return funnel


@router.get("", response_model=list[FunnelRead])
async def list_funnels(
    session: DbSession,
    user: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[FunnelRead]:
    return await FunnelService(session).list(user_id=user.id, project_id=project_id)


@router.get("/{funnel_id}/results", response_model=FunnelResult)
async def funnel_results(
    funnel_id: str,
    session: DbSession,
    user: CurrentUser,
) -> FunnelResult:
    return await FunnelService(session).results(funnel_id=funnel_id, user_id=user.id)
