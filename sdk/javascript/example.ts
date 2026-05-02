type EventPayload = {
  event_name: string;
  user_id?: string;
  anonymous_id?: string;
  timestamp?: string;
  properties?: Record<string, unknown>;
  context?: Record<string, unknown>;
};

class EventPipelineClient {
  constructor(
    private readonly apiUrl: string,
    private readonly apiKey: string,
  ) {}

  async track(event: EventPayload) {
    return this.post("/events/track", event);
  }

  async batchTrack(events: EventPayload[]) {
    return this.post("/events/batch", { events });
  }

  private async post(path: string, payload: unknown) {
    const response = await fetch(`${this.apiUrl.replace(/\/$/, "")}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": this.apiKey,
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      return { accepted: false, status: response.status };
    }
    return response.json();
  }
}

const client = new EventPipelineClient(
  "http://localhost:8000/api/v1",
  "sk_live_demo_event_pipeline_key",
);

void client.track({
  event_name: "document_uploaded",
  user_id: "user_123",
  properties: { file_type: "pdf", file_size_mb: 2.4, source: "dashboard" },
  context: { country: "DE", user_agent: "browser" },
});
