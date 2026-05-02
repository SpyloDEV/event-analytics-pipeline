import asyncio
from datetime import UTC, datetime, timedelta

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.api_key import ApiKey
from app.models.audit_log import AuditLog
from app.models.enums import (
    AnomalySeverity,
    ApiKeyStatus,
    IngestionStatus,
    PipelineLogLevel,
    ProjectRole,
    UserRole,
)
from app.models.event import Anomaly, EventSchema, Funnel, PipelineLog, RawEvent
from app.models.user import User
from app.models.workspace import Organization, Project, ProjectMember
from app.services.api_key_service import hash_api_key


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        user = User(
            email="platform@example.com",
            full_name="Analytics Platform Owner",
            hashed_password=hash_password("SecurePass123!"),
            role=UserRole.OWNER,
        )
        session.add(user)
        await session.flush()

        organization = Organization(
            name="SpyloDEV Data Platform",
            slug="spylodev-data-platform",
            created_by=user.id,
        )
        session.add(organization)
        await session.flush()

        project = Project(
            organization_id=organization.id,
            name="Product Analytics",
            key="product-analytics",
            description="Product event pipeline for web and backend apps.",
        )
        session.add(project)
        await session.flush()
        session.add(
            ProjectMember(
                project_id=project.id,
                user_id=user.id,
                role=ProjectRole.OWNER,
            )
        )

        api_secret = "sk_live_demo_event_pipeline_key"
        api_key = ApiKey(
            project_id=project.id,
            name="Production Ingestion",
            key_hash=hash_api_key(api_secret),
            key_prefix=api_secret[:12],
            scopes=["events:write"],
            status=ApiKeyStatus.ACTIVE,
        )
        session.add(api_key)

        schemas = [
            EventSchema(
                project_id=project.id,
                event_name="document_uploaded",
                required_properties={"file_type": "string", "file_size_mb": "number"},
                optional_properties={"source": "string"},
                property_types={"file_type": "string", "file_size_mb": "number"},
            ),
            EventSchema(
                project_id=project.id,
                event_name="workflow_executed",
                required_properties={"workflow_type": "string"},
                optional_properties={"source": "string"},
                property_types={"workflow_type": "string"},
            ),
        ]
        session.add_all(schemas)
        await session.flush()

        now = datetime.now(UTC)
        event_names = [
            "user_signed_up",
            "user_logged_in",
            "page_viewed",
            "button_clicked",
            "document_uploaded",
            "workflow_executed",
            "payment_failed",
        ]
        for index in range(60):
            event_name = event_names[index % len(event_names)]
            session.add(
                RawEvent(
                    project_id=project.id,
                    event_name=event_name,
                    user_id=f"user_{index % 18}",
                    anonymous_id=f"anon_{index}",
                    timestamp=now - timedelta(hours=index),
                    properties={
                        "source": "dashboard" if index % 2 == 0 else "website",
                        "file_type": "pdf",
                        "file_size_mb": 2.4,
                    },
                    context={
                        "country": "DE" if index % 3 == 0 else "US",
                        "user_agent": "browser",
                    },
                    ingestion_status=IngestionStatus.PROCESSED,
                    validation_errors=[],
                )
            )
        await session.flush()

        funnel = Funnel(
            project_id=project.id,
            name="Activation Funnel",
            steps=["user_signed_up", "document_uploaded", "workflow_executed"],
        )
        anomaly = Anomaly(
            project_id=project.id,
            title="Payment failure spike",
            severity=AnomalySeverity.HIGH,
            signal="event_volume_spike",
            metadata_json={"event_name": "payment_failed", "change": "+184%"},
        )
        session.add_all([funnel, anomaly])

        session.add_all(
            [
                PipelineLog(
                    project_id=project.id,
                    level=PipelineLogLevel.INFO,
                    message="event received",
                    event_name="document_uploaded",
                    metadata_json={"source": "seed"},
                ),
                PipelineLog(
                    project_id=project.id,
                    level=PipelineLogLevel.INFO,
                    message="aggregation updated",
                    event_name="workflow_executed",
                    metadata_json={"source": "seed"},
                ),
                AuditLog(
                    organization_id=organization.id,
                    project_id=project.id,
                    actor_id=user.id,
                    action="schema_created",
                    target_type="schema",
                    target_id=schemas[0].id,
                    metadata_json={"seeded": True},
                ),
                AuditLog(
                    organization_id=organization.id,
                    project_id=project.id,
                    actor_id=user.id,
                    action="api_key_created",
                    target_type="api_key",
                    target_id=api_key.id,
                    metadata_json={"seeded": True},
                ),
            ]
        )
        await session.commit()
        print("Seeded demo analytics pipeline.")
        print(f"Demo login: {user.email} / SecurePass123!")
        print(f"Demo API key: {api_secret}")


if __name__ == "__main__":
    asyncio.run(seed())
