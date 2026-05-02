import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const logs = [
  { action: "schema_created", actor: "platform@example.com", target: "document_uploaded", time: "4 min ago" },
  { action: "api_key_created", actor: "platform@example.com", target: "Production Ingestion", time: "18 min ago" },
  { action: "event_rejected", actor: "pipeline", target: "document_uploaded", time: "22 min ago" },
  { action: "anomaly_detected", actor: "pipeline", target: "payment_failed", time: "41 min ago" },
];

export default function AuditLogsPage() {
  return (
    <DashboardShell
      title="Audit Logs"
      description="Review project, API key, schema, rejected event, and anomaly actions across the analytics platform."
    >
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Action</Th>
                <Th>Actor</Th>
                <Th>Target</Th>
                <Th>Time</Th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={`${log.action}-${log.time}`}>
                  <Td className="font-medium">{log.action}</Td>
                  <Td>{log.actor}</Td>
                  <Td>{log.target}</Td>
                  <Td className="text-muted-foreground">{log.time}</Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}
