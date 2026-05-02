from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import install_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        summary="Event analytics and pipeline API for product tracking, schema validation, aggregation, anomaly detection, and dashboards.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        openapi_tags=[
            {"name": "Authentication", "description": "JWT login and identity."},
            {"name": "Organizations", "description": "Organizations and ownership."},
            {"name": "Projects", "description": "Product analytics projects."},
            {"name": "API Keys", "description": "Scoped ingestion credentials."},
            {"name": "Events", "description": "Track and inspect product events."},
            {"name": "Schemas", "description": "Event contract registry."},
            {"name": "Analytics", "description": "Aggregates and dashboard metrics."},
            {"name": "Funnels", "description": "Conversion funnel definitions."},
            {"name": "Anomalies", "description": "Pipeline anomaly detection."},
            {
                "name": "Pipeline",
                "description": "Validation and aggregation observability.",
            },
            {"name": "Audit Logs", "description": "Administrative activity trail."},
        ],
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    install_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["Health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    return app


app = create_app()
