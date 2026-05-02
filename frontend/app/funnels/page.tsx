import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, Td, Th } from "@/components/ui/table";

const steps = [
  { event: "user_signed_up", count: "42,810", conversion: "100%" },
  { event: "document_uploaded", count: "24,204", conversion: "56.5%" },
  { event: "workflow_executed", count: "18,902", conversion: "44.1%" },
];

export default function FunnelsPage() {
  return (
    <DashboardShell
      title="Funnels"
      description="Build and monitor conversion paths from product events with drop-off and conversion rates."
      action={<Button>Create Funnel</Button>}
    >
      <div className="grid gap-4 xl:grid-cols-[0.7fr_1.3fr]">
        <Card>
          <CardHeader>
            <CardTitle>Funnel Builder</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input defaultValue="Activation Funnel" aria-label="Funnel name" />
            <Input defaultValue="user_signed_up" aria-label="Step one" />
            <Input defaultValue="document_uploaded" aria-label="Step two" />
            <Input defaultValue="workflow_executed" aria-label="Step three" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Activation Funnel</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Step</Th>
                  <Th>Users</Th>
                  <Th>Conversion</Th>
                </tr>
              </thead>
              <tbody>
                {steps.map((step) => (
                  <tr key={step.event}>
                    <Td className="font-mono">{step.event}</Td>
                    <Td>{step.count}</Td>
                    <Td>
                      <Badge tone="processing">{step.conversion}</Badge>
                    </Td>
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
