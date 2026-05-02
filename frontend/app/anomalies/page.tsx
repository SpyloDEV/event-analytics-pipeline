import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const anomalies = [
  { title: "Payment failure spike", severity: "high", signal: "+184% hourly volume" },
  { title: "Validation error rate", severity: "medium", signal: "document_uploaded missing file_size_mb" },
  { title: "Missing expected event", severity: "low", signal: "button_clicked below baseline" },
];

export default function AnomaliesPage() {
  return (
    <DashboardShell
      title="Anomalies"
      description="Monitor event volume spikes, drops, validation error bursts, and missing expected events."
    >
      <div className="grid gap-4 md:grid-cols-3">
        {anomalies.map((anomaly) => (
          <Card key={anomaly.title}>
            <CardHeader>
              <CardTitle className="text-base">{anomaly.title}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Badge tone={anomaly.severity === "high" ? "blocked" : "warning"}>
                {anomaly.severity}
              </Badge>
              <p className="text-sm text-muted-foreground">{anomaly.signal}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </DashboardShell>
  );
}
