import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const keys = [
  { name: "Production Ingestion", prefix: "sk_live_a9f2", scope: "events:write", status: "active" },
  { name: "Mobile SDK", prefix: "sk_live_7c21", scope: "events:write", status: "active" },
  { name: "Legacy Web", prefix: "sk_live_1b90", scope: "events:write", status: "revoked" },
];

export default function ApiKeysPage() {
  return (
    <DashboardShell
      title="API Keys"
      description="Issue scoped ingestion credentials for web, mobile, backend, and server-side SDK event tracking."
      action={<Button>Create API Key</Button>}
    >
      <Card>
        <CardHeader>
          <CardTitle>Ingestion Credentials</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Name</Th>
                <Th>Prefix</Th>
                <Th>Scope</Th>
                <Th>Status</Th>
              </tr>
            </thead>
            <tbody>
              {keys.map((key) => (
                <tr key={key.prefix}>
                  <Td className="font-medium">{key.name}</Td>
                  <Td className="font-mono">{key.prefix}...</Td>
                  <Td>{key.scope}</Td>
                  <Td>
                    <Badge tone={key.status === "active" ? "active" : "revoked"}>
                      {key.status}
                    </Badge>
                  </Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}
