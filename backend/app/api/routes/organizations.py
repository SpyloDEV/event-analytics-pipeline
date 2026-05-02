from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.services.project_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    session: DbSession,
    user: CurrentUser,
) -> OrganizationRead:
    organization = await OrganizationService(session).create(
        user_id=user.id,
        name=payload.name,
    )
    await session.commit()
    await session.refresh(organization)
    return organization


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    session: DbSession,
    user: CurrentUser,
) -> list[OrganizationRead]:
    return await OrganizationService(session).list(user_id=user.id)
