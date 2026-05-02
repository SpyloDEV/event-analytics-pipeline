from fastapi import APIRouter

from app.api.routes import (
    analytics,
    anomalies,
    api_keys,
    audit_logs,
    auth,
    events,
    funnels,
    organizations,
    pipeline,
    projects,
    schemas,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(projects.router)
api_router.include_router(api_keys.router)
api_router.include_router(events.router)
api_router.include_router(schemas.router)
api_router.include_router(analytics.router)
api_router.include_router(funnels.router)
api_router.include_router(anomalies.router)
api_router.include_router(pipeline.router)
api_router.include_router(audit_logs.router)
