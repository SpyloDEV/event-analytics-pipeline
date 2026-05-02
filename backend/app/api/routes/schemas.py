from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.common import Message
from app.schemas.event import EventSchemaCreate, EventSchemaRead, EventSchemaUpdate
from app.services.schema_service import SchemaService

router = APIRouter(prefix="/schemas", tags=["Schemas"])


@router.post("", response_model=EventSchemaRead, status_code=status.HTTP_201_CREATED)
async def create_schema(
    payload: EventSchemaCreate,
    session: DbSession,
    user: CurrentUser,
) -> EventSchemaRead:
    schema = await SchemaService(session).create(
        user_id=user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(schema)
    return schema


@router.get("", response_model=list[EventSchemaRead])
async def list_schemas(
    session: DbSession,
    user: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[EventSchemaRead]:
    return await SchemaService(session).list(user_id=user.id, project_id=project_id)


@router.get("/{schema_id}", response_model=EventSchemaRead)
async def get_schema(
    schema_id: str,
    session: DbSession,
    user: CurrentUser,
) -> EventSchemaRead:
    return await SchemaService(session).get(schema_id=schema_id, user_id=user.id)


@router.patch("/{schema_id}", response_model=EventSchemaRead)
async def update_schema(
    schema_id: str,
    payload: EventSchemaUpdate,
    session: DbSession,
    user: CurrentUser,
) -> EventSchemaRead:
    schema = await SchemaService(session).update(
        schema_id=schema_id,
        user_id=user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(schema)
    return schema


@router.delete("/{schema_id}", response_model=Message)
async def delete_schema(
    schema_id: str, session: DbSession, user: CurrentUser
) -> Message:
    schema = await SchemaService(session).get(schema_id=schema_id, user_id=user.id)
    await session.delete(schema)
    await session.commit()
    return Message(message="Schema deleted.")
