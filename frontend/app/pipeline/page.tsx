import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const logs = [
  { level: "info", message: "event received", event: "document_uploaded" },
  { level: "info", message: "validation passed", event: "document_uploaded" },
  { level: "info", message: "aggregation updated", event: "workflow_executed" },
  { level: "error", message: "validation failed", event: "document_uploaded" },
];

export default function PipelinePage() {
  return (
    <DashboardShell
      title="Pipeline"
      description="Observe ingestion health, validation flow, worker lag, pipeline logs, and aggregate freshness."
    >
      <div className="grid gap-4 xl:grid-cols-[0.7fr_1.3fr]">
        <Card>
          <CardHeader>
            <CardTitle>Health</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Badge tone="active">healthy</Badge>
            <p className="text-sm text-muted-foreground">Redis connected, worker lag 2s, ingestion API accepting traffic.</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recent Logs</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Level</Th>
                  <Th>Message</Th>
                  <Th>Event</Th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, index) => (
                  <tr key={`${log.message}-${index}`}>
                    <Td>
                      <Badge tone={log.level === "error" ? "blocked" : "active"}>{log.level}</Badge>
                    </Td>
                    <Td>{log.message}</Td>
                    <Td className="font-mono">{log.event}</Td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
