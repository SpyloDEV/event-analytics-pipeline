from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.enums import AnomalySeverity, AnomalyStatus
from app.models.event import Anomaly
from app.repositories.analytics import AnalyticsRepository


class AnomalyService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)

    async def detect_for_project(self, project_id: str) -> list[Anomaly]:
        events = await self.repository.list_raw_events(project_id=project_id, limit=500)
        failed = [event for event in events if event.validation_errors]
        anomalies = []
        if len(events) > 100:
            anomalies.append(
                await self.repository.create_anomaly(
                    {
                        "project_id": project_id,
                        "title": "Event volume spike detected",
                        "severity": AnomalySeverity.MEDIUM,
                        "signal": "volume_spike",
                        "metadata_json": {"sample_size": len(events)},
                    }
                )
            )
        if events and len(failed) / len(events) > 0.2:
            anomalies.append(
                await self.repository.create_anomaly(
                    {
                        "project_id": project_id,
                        "title": "High validation error rate",
                        "severity": AnomalySeverity.HIGH,
                        "signal": "validation_error_rate",
                        "metadata_json": {"failed_events": len(failed)},
                    }
                )
            )
        return anomalies

    async def list(self, *, project_id: str | None = None) -> list[Anomaly]:
        return list(await self.repository.list_anomalies(project_id=project_id))

    async def resolve(self, *, anomaly_id: str) -> Anomaly:
        anomaly = await self.repository.get_anomaly(anomaly_id)
        if anomaly is None:
            raise NotFoundError("Anomaly not found.")
        anomaly.status = AnomalyStatus.RESOLVED
        return anomaly
