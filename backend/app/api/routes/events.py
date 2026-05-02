from fastapi import APIRouter, Header, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.models.enums import IngestionStatus
from app.schemas.event import (
    BatchEventRequest,
    BatchEventResponse,
    RawEventRead,
    TrackEventRequest,
    TrackEventResponse,
)
from app.services.api_key_service import ApiKeyService
from app.services.event_service import EventService
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "/track", response_model=TrackEventResponse, status_code=status.HTTP_202_ACCEPTED
)
async def track_event(
    payload: TrackEventRequest,
    session: DbSession,
    x_api_key: str = Header(alias="X-API-Key"),
) -> TrackEventResponse:
    api_key = await ApiKeyService(session).authenticate(x_api_key)
    event = await IngestionService(session).track(api_key=api_key, payload=payload)
    await session.commit()
    return TrackEventResponse(event_id=event.id, status=event.ingestion_status)


@router.post(
    "/batch", response_model=BatchEventResponse, status_code=status.HTTP_202_ACCEPTED
)
async def batch_events(
    payload: BatchEventRequest,
    session: DbSession,
    x_api_key: str = Header(alias="X-API-Key"),
) -> BatchEventResponse:
    api_key = await ApiKeyService(session).authenticate(x_api_key)
    events = await IngestionService(session).batch(
        api_key=api_key, events=payload.events
    )
    await session.commit()
    return BatchEventResponse(
        accepted_count=len(events),
        event_ids=[event.id for event in events],
    )


@router.get("", response_model=list[RawEventRead])
async def list_events(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[RawEventRead]:
    return await EventService(session).list(project_id=project_id, limit=limit)


@router.get("/failed", response_model=list[RawEventRead])
async def failed_events(
    session: DbSession,
    _: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[RawEventRead]:
    return await EventService(session).list(project_id=project_id, failed_only=True)


@router.get("/{event_id}", response_model=RawEventRead)
async def get_event(event_id: str, session: DbSession, _: CurrentUser) -> RawEventRead:
    event = await EventService(session).get(event_id=event_id)
    if event.ingestion_status == IngestionStatus.REJECTED:
        return event
    return event
