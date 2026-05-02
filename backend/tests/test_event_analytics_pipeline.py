from httpx import AsyncClient

from tests.conftest import create_api_key, create_organization, create_project


async def _project(client: AsyncClient, headers: dict[str, str]) -> dict:
    organization = await create_organization(client, headers)
    return await create_project(client, headers, organization["id"])


async def test_project_api_key_and_event_ingestion(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    project = await _project(client, auth_headers)
    secret = await create_api_key(client, auth_headers, project["id"])

    response = await client.post(
        "/api/v1/events/track",
        headers={"X-API-Key": secret},
        json={
            "event_name": "document_uploaded",
            "user_id": "user_123",
            "anonymous_id": "anon_456",
            "properties": {
                "file_type": "pdf",
                "file_size_mb": 2.4,
                "source": "dashboard",
            },
            "context": {"country": "DE", "user_agent": "browser"},
        },
    )

    assert response.status_code == 202, response.text
    assert response.json()["status"] == "processed"


async def test_schema_validation_marks_failed_event(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    project = await _project(client, auth_headers)
    secret = await create_api_key(client, auth_headers, project["id"])
    schema = await client.post(
        "/api/v1/schemas",
        headers=auth_headers,
        json={
            "project_id": project["id"],
            "event_name": "document_uploaded",
            "required_properties": {"file_type": "string", "file_size_mb": "number"},
            "property_types": {"file_type": "string", "file_size_mb": "number"},
        },
    )
    assert schema.status_code == 201, schema.text

    event = await client.post(
        "/api/v1/events/track",
        headers={"X-API-Key": secret},
        json={
            "event_name": "document_uploaded",
            "user_id": "user_123",
            "properties": {"file_type": "pdf"},
            "context": {"country": "DE"},
        },
    )
    failed = await client.get(
        "/api/v1/events/failed",
        headers=auth_headers,
        params={"project_id": project["id"]},
    )

    assert event.status_code == 202, event.text
    assert event.json()["status"] == "failed"
    assert failed.status_code == 200, failed.text
    assert len(failed.json()) == 1


async def test_batch_ingestion_and_analytics(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    project = await _project(client, auth_headers)
    secret = await create_api_key(client, auth_headers, project["id"])
    response = await client.post(
        "/api/v1/events/batch",
        headers={"X-API-Key": secret},
        json={
            "events": [
                {
                    "event_name": "user_signed_up",
                    "user_id": "user_1",
                    "properties": {"source": "landing"},
                    "context": {"country": "US"},
                },
                {
                    "event_name": "workflow_executed",
                    "user_id": "user_1",
                    "properties": {"source": "dashboard"},
                    "context": {"country": "US"},
                },
            ]
        },
    )
    overview = await client.get(
        "/api/v1/analytics/overview",
        headers=auth_headers,
        params={"project_id": project["id"]},
    )

    assert response.status_code == 202, response.text
    assert response.json()["accepted_count"] == 2
    assert overview.status_code == 200, overview.text
    assert overview.json()["total_events"] == 2
    assert overview.json()["unique_users"] == 1


async def test_funnel_calculation(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    project = await _project(client, auth_headers)
    secret = await create_api_key(client, auth_headers, project["id"])
    await client.post(
        "/api/v1/events/batch",
        headers={"X-API-Key": secret},
        json={
            "events": [
                {"event_name": "user_signed_up", "user_id": "u1"},
                {"event_name": "document_uploaded", "user_id": "u1"},
                {"event_name": "workflow_executed", "user_id": "u1"},
            ]
        },
    )
    funnel = await client.post(
        "/api/v1/funnels",
        headers=auth_headers,
        json={
            "project_id": project["id"],
            "name": "Activation",
            "steps": ["user_signed_up", "document_uploaded", "workflow_executed"],
        },
    )
    results = await client.get(
        f"/api/v1/funnels/{funnel.json()['id']}/results", headers=auth_headers
    )

    assert funnel.status_code == 201, funnel.text
    assert results.status_code == 200, results.text
    assert results.json()["overall_conversion_rate"] == 100


async def test_audit_logs_and_pipeline_logs(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    project = await _project(client, auth_headers)
    secret = await create_api_key(client, auth_headers, project["id"])
    await client.post(
        "/api/v1/events/track",
        headers={"X-API-Key": secret},
        json={"event_name": "page_viewed", "anonymous_id": "anon_123"},
    )
    audit = await client.get(
        "/api/v1/audit-logs",
        headers=auth_headers,
        params={"project_id": project["id"]},
    )
    pipeline = await client.get(
        "/api/v1/pipeline/logs",
        headers=auth_headers,
        params={"project_id": project["id"]},
    )

    assert audit.status_code == 200, audit.text
    assert any(item["action"] == "api_key_created" for item in audit.json())
    assert pipeline.status_code == 200, pipeline.text
    assert any(item["message"] == "event received" for item in pipeline.json())
