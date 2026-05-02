from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.api_key import ApiKeyCreate, ApiKeyCreated, ApiKeyRead
from app.services.api_key_service import ApiKeyService

router = APIRouter(prefix="/api-keys", tags=["API Keys"])


@router.post("", response_model=ApiKeyCreated, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    payload: ApiKeyCreate,
    session: DbSession,
    user: CurrentUser,
) -> ApiKeyCreated:
    api_key, secret = await ApiKeyService(session).create(
        user_id=user.id,
        data=payload.model_dump(),
    )
    await session.commit()
    await session.refresh(api_key)
    return ApiKeyCreated(
        **ApiKeyRead.model_validate(api_key).model_dump(),
        secret=secret,
    )


@router.get("", response_model=list[ApiKeyRead])
async def list_api_keys(
    session: DbSession,
    user: CurrentUser,
    project_id: str | None = Query(default=None),
) -> list[ApiKeyRead]:
    return await ApiKeyService(session).list(user_id=user.id, project_id=project_id)


@router.patch("/{api_key_id}/revoke", response_model=ApiKeyRead)
async def revoke_api_key(
    api_key_id: str,
    session: DbSession,
    user: CurrentUser,
) -> ApiKeyRead:
    api_key = await ApiKeyService(session).revoke(
        api_key_id=api_key_id,
        user_id=user.id,
    )
    await session.commit()
    await session.refresh(api_key)
    return api_key
