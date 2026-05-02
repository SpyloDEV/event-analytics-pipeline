from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.process_event")
def process_event(event_id: str) -> dict[str, str]:
    return {"event_id": event_id, "status": "queued_for_processing"}


@celery_app.task(name="app.workers.tasks.refresh_aggregates")
def refresh_aggregates(project_id: str) -> dict[str, str]:
    return {"project_id": project_id, "status": "aggregates_refreshed"}
