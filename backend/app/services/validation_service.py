from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import IngestionStatus, PipelineLogLevel
from app.models.event import RawEvent
from app.repositories.analytics import AnalyticsRepository
from app.services.pipeline_log_service import PipelineLogService


class ValidationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalyticsRepository(session)
        self.pipeline_logs = PipelineLogService(session)

    async def validate_event(self, event: RawEvent) -> RawEvent:
        await self.pipeline_logs.write(
            project_id=event.project_id,
            raw_event_id=event.id,
            event_name=event.event_name,
            message="schema validation started",
        )
        schema = await self.repository.get_schema(
            project_id=event.project_id,
            event_name=event.event_name,
        )
        if schema is None:
            event.ingestion_status = IngestionStatus.PROCESSED
            await self.pipeline_logs.write(
                project_id=event.project_id,
                raw_event_id=event.id,
                event_name=event.event_name,
                message="validation passed without registered schema",
            )
            return event
        errors = self._validate_properties(
            properties=event.properties,
            required=schema.required_properties,
            property_types=schema.property_types,
        )
        event.validation_errors = errors
        event.ingestion_status = (
            IngestionStatus.FAILED if errors else IngestionStatus.PROCESSED
        )
        await self.pipeline_logs.write(
            project_id=event.project_id,
            raw_event_id=event.id,
            event_name=event.event_name,
            level=PipelineLogLevel.ERROR if errors else PipelineLogLevel.INFO,
            message="validation failed" if errors else "validation passed",
            metadata={"errors": errors},
        )
        return event

    def _validate_properties(
        self,
        *,
        properties: dict[str, Any],
        required: dict[str, str],
        property_types: dict[str, str],
    ) -> list[dict[str, str]]:
        errors: list[dict[str, str]] = []
        for key in required:
            if key not in properties:
                errors.append({"field": key, "message": "required property missing"})
        for key, expected_type in property_types.items():
            if key in properties and not self._matches_type(
                properties[key], expected_type
            ):
                errors.append(
                    {
                        "field": key,
                        "message": f"expected {expected_type}",
                    }
                )
        return errors

    def _matches_type(self, value: Any, expected_type: str) -> bool:
        checks = {
            "string": lambda item: isinstance(item, str),
            "number": lambda item: isinstance(item, int | float)
            and not isinstance(item, bool),
            "boolean": lambda item: isinstance(item, bool),
            "object": lambda item: isinstance(item, dict),
            "array": lambda item: isinstance(item, list),
        }
        return checks.get(expected_type, lambda _: True)(value)
