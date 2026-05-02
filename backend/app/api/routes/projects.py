from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.organization import ProjectCreate, ProjectRead
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    session: DbSession,
    user: CurrentUser,
) -> ProjectRead:
    project = await ProjectService(session).create(
        user_id=user.id,
        data=payload.model_dump(),
    )
    await session.commit()
    await session.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(session: DbSession, user: CurrentUser) -> list[ProjectRead]:
    return await ProjectService(session).list(user_id=user.id)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: str,
    session: DbSession,
    user: CurrentUser,
) -> ProjectRead:
    return await ProjectService(session).get(project_id=project_id, user_id=user.id)
