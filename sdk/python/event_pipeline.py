from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib import request


@dataclass(slots=True)
class EventPipelineClient:
    api_url: str
    api_key: str
    timeout_seconds: int = 3

    def track(
        self,
        event_name: str,
        user_id: str | None = None,
        properties: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._post(
            "/events/track",
            {
                "event_name": event_name,
                "user_id": user_id,
                "timestamp": datetime.now(UTC).isoformat(),
                "properties": properties or {},
                "context": context or {},
            },
        )

    def batch_track(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        return self._post("/events/batch", {"events": events})

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode()
        http_request = request.Request(
            f"{self.api_url.rstrip('/')}{path}",
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            },
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode())
        except Exception as exc:
            return {"accepted": False, "error": str(exc)}


if __name__ == "__main__":
    client = EventPipelineClient(
        api_url="http://localhost:8000/api/v1",
        api_key="sk_live_demo_event_pipeline_key",
    )
    print(
        client.track(
            "document_uploaded",
            user_id="user_123",
            properties={"file_type": "pdf", "file_size_mb": 2.4, "source": "dashboard"},
            context={"country": "DE", "user_agent": "browser"},
        )
    )
