from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_events: int
    unique_users: int
    events_today: int
    top_event: str | None
    ingestion_error_rate: float
    events_over_time: list[dict]
    top_events: list[dict]
    countries: list[dict]
    sources: list[dict]
