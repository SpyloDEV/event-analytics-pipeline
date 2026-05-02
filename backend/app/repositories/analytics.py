from collections.abc import Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.api_key import ApiKey
from app.models.audit_log import AuditLog
from app.models.enums import ApiKeyStatus, IngestionStatus
from app.models.event import Anomaly, EventSchema, Funnel, PipelineLog, RawEvent
from app.models.workspace import Organization, Project, ProjectMember


class AnalyticsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_organization(self, organization_id: str) -> Organization | None:
        return await self.session.get(Organization, organization_id)

    async def list_organizations(self, user_id: str) -> Sequence[Organization]:
        result = await self.session.execute(
            select(Organization).where(Organization.created_by == user_id)
        )
        return result.scalars().all()

    async def create_organization(self, data: dict) -> Organization:
        organization = Organization(**data)
        self.session.add(organization)
        await self.session.flush()
        return organization

    async def get_project(self, project_id: str) -> Project | None:
        return await self.session.get(Project, project_id)

    async def get_project_for_user(
        self, project_id: str, user_id: str
    ) -> Project | None:
        result = await self.session.execute(
            select(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(Project.id == project_id, ProjectMember.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_projects(self, user_id: str) -> Sequence[Project]:
        result = await self.session.execute(
            select(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(ProjectMember.user_id == user_id)
            .order_by(Project.created_at.desc())
        )
        return result.scalars().all()

    async def create_project(self, data: dict) -> Project:
        project = Project(**data)
        self.session.add(project)
        await self.session.flush()
        return project

    async def create_project_member(self, data: dict) -> ProjectMember:
        member = ProjectMember(**data)
        self.session.add(member)
        await self.session.flush()
        return member

    async def get_project_member(
        self, *, project_id: str, user_id: str
    ) -> ProjectMember | None:
        result = await self.session.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create_api_key(self, data: dict) -> ApiKey:
        api_key = ApiKey(**data)
        self.session.add(api_key)
        await self.session.flush()
        return api_key

    async def get_api_key_by_hash(self, key_hash: str) -> ApiKey | None:
        result = await self.session.execute(
            select(ApiKey).where(
                ApiKey.key_hash == key_hash,
                ApiKey.status == ApiKeyStatus.ACTIVE,
            )
        )
        return result.scalar_one_or_none()

    async def get_api_key(self, api_key_id: str) -> ApiKey | None:
        return await self.session.get(ApiKey, api_key_id)

    async def list_api_keys(self, project_id: str | None = None) -> Sequence[ApiKey]:
        query = select(ApiKey).order_by(ApiKey.created_at.desc())
        if project_id:
            query = query.where(ApiKey.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_raw_event(self, data: dict) -> RawEvent:
        event = RawEvent(**data)
        self.session.add(event)
        await self.session.flush()
        return event

    async def get_raw_event(self, event_id: str) -> RawEvent | None:
        return await self.session.get(RawEvent, event_id)

    async def list_raw_events(
        self,
        *,
        project_id: str | None = None,
        status: IngestionStatus | None = None,
        limit: int = 100,
    ) -> Sequence[RawEvent]:
        query: Select[tuple[RawEvent]] = (
            select(RawEvent).order_by(RawEvent.timestamp.desc()).limit(limit)
        )
        if project_id:
            query = query.where(RawEvent.project_id == project_id)
        if status:
            query = query.where(RawEvent.ingestion_status == status)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_schema(
        self, *, project_id: str, event_name: str
    ) -> EventSchema | None:
        result = await self.session.execute(
            select(EventSchema).where(
                EventSchema.project_id == project_id,
                EventSchema.event_name == event_name,
                EventSchema.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def get_schema_by_id(self, schema_id: str) -> EventSchema | None:
        return await self.session.get(EventSchema, schema_id)

    async def create_schema(self, data: dict) -> EventSchema:
        schema = EventSchema(**data)
        self.session.add(schema)
        await self.session.flush()
        return schema

    async def list_schemas(
        self, project_id: str | None = None
    ) -> Sequence[EventSchema]:
        query = select(EventSchema).order_by(EventSchema.created_at.desc())
        if project_id:
            query = query.where(EventSchema.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_funnel(self, data: dict) -> Funnel:
        funnel = Funnel(**data)
        self.session.add(funnel)
        await self.session.flush()
        return funnel

    async def get_funnel(self, funnel_id: str) -> Funnel | None:
        return await self.session.get(Funnel, funnel_id)

    async def list_funnels(self, project_id: str | None = None) -> Sequence[Funnel]:
        query = select(Funnel).order_by(Funnel.created_at.desc())
        if project_id:
            query = query.where(Funnel.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_anomaly(self, data: dict) -> Anomaly:
        anomaly = Anomaly(**data)
        self.session.add(anomaly)
        await self.session.flush()
        return anomaly

    async def get_anomaly(self, anomaly_id: str) -> Anomaly | None:
        return await self.session.get(Anomaly, anomaly_id)

    async def list_anomalies(self, project_id: str | None = None) -> Sequence[Anomaly]:
        query = select(Anomaly).order_by(Anomaly.created_at.desc())
        if project_id:
            query = query.where(Anomaly.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_pipeline_log(self, data: dict) -> PipelineLog:
        log = PipelineLog(**data)
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_pipeline_logs(
        self, *, project_id: str | None = None, limit: int = 100
    ) -> Sequence[PipelineLog]:
        query = select(PipelineLog).order_by(PipelineLog.created_at.desc()).limit(limit)
        if project_id:
            query = query.where(PipelineLog.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_audit_log(self, data: dict) -> AuditLog:
        audit_log = AuditLog(**data)
        self.session.add(audit_log)
        await self.session.flush()
        return audit_log

    async def list_audit_logs(
        self, *, project_id: str | None = None, limit: int = 100
    ) -> Sequence[AuditLog]:
        query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        if project_id:
            query = query.where(AuditLog.project_id == project_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def overview(self, project_id: str | None = None) -> dict:
        event_query = select(func.count()).select_from(RawEvent)
        failed_query = (
            select(func.count())
            .select_from(RawEvent)
            .where(
                RawEvent.ingestion_status.in_(
                    [IngestionStatus.FAILED, IngestionStatus.REJECTED]
                )
            )
        )
        user_query = select(func.count(func.distinct(RawEvent.user_id))).select_from(
            RawEvent
        )
        top_query = select(RawEvent.event_name, func.count()).group_by(
            RawEvent.event_name
        )
        if project_id:
            event_query = event_query.where(RawEvent.project_id == project_id)
            failed_query = failed_query.where(RawEvent.project_id == project_id)
            user_query = user_query.where(RawEvent.project_id == project_id)
            top_query = top_query.where(RawEvent.project_id == project_id)
        total_events = await self.session.scalar(event_query) or 0
        failed_events = await self.session.scalar(failed_query) or 0
        unique_users = await self.session.scalar(user_query) or 0
        top_result = await self.session.execute(top_query.order_by(func.count().desc()))
        top_events = [
            {"event_name": row[0], "count": row[1]} for row in top_result.all()
        ]
        return {
            "total_events": total_events,
            "unique_users": unique_users,
            "events_today": total_events,
            "top_event": top_events[0]["event_name"] if top_events else None,
            "ingestion_error_rate": (
                round((failed_events / total_events * 100), 2) if total_events else 0
            ),
            "top_events": top_events[:10],
        }
