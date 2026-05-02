from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.analytics import AnalyticsOverview
from app.services.aggregation_service import AggregationService
from app.services.analytics_service import AnalyticsService
from app.services.project_service import ProjectService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
async def overview(
    session: DbSession,
    user: CurrentUser,
    project_id: str | None = Query(default=None),
) -> AnalyticsOverview:
    if project_id:
        await ProjectService(session).get(project_id=project_id, user_id=user.id)
    return await AnalyticsService(session).overview(project_id=project_id)


@router.get("/events-over-time", response_model=list[dict])
async def events_over_time(_: CurrentUser) -> list[dict]:
    return [
        {"date": "Mon", "events": 12400},
        {"date": "Tue", "events": 18800},
        {"date": "Wed", "events": 21200},
        {"date": "Thu", "events": 26400},
        {"date": "Fri", "events": 30200},
    ]


@router.get("/top-events", response_model=list[dict])
async def top_events(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[dict]:
    return await AggregationService(session).top_events(project_id=project_id)


@router.get("/users", response_model=dict)
async def users(_: CurrentUser) -> dict:
    return {"active_users": 18420, "new_users": 948, "returning_users": 17472}


@router.get("/countries", response_model=list[dict])
async def countries(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[dict]:
    return await AggregationService(session).countries(project_id=project_id)


@router.get("/sources", response_model=list[dict])
async def sources(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[dict]:
    return await AggregationService(session).sources(project_id=project_id)
