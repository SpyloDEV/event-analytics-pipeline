import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, Td, Th } from "@/components/ui/table";

const schemas = [
  { event: "document_uploaded", required: "file_type, file_size_mb", status: "active" },
  { event: "workflow_executed", required: "workflow_type", status: "active" },
  { event: "payment_failed", required: "amount, provider", status: "draft" },
];

export default function SchemasPage() {
  return (
    <DashboardShell
      title="Schema Registry"
      description="Define expected event contracts, required properties, optional fields, and runtime validation rules."
      action={<Button>Create Schema</Button>}
    >
      <div className="grid gap-4 xl:grid-cols-[0.8fr_1.2fr]">
        <Card>
          <CardHeader>
            <CardTitle>Schema Builder</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input defaultValue="document_uploaded" aria-label="Event name" />
            <Input defaultValue="file_type:string" aria-label="Required property" />
            <Input defaultValue="file_size_mb:number" aria-label="Property type" />
            <Button className="w-full">Save Schema</Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Registered Schemas</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <thead>
                <tr>
                  <Th>Event</Th>
                  <Th>Required Properties</Th>
                  <Th>Status</Th>
                </tr>
              </thead>
              <tbody>
                {schemas.map((schema) => (
                  <tr key={schema.event}>
                    <Td className="font-mono">{schema.event}</Td>
                    <Td>{schema.required}</Td>
                    <Td>
                      <Badge tone={schema.status === "active" ? "active" : "draft"}>
                        {schema.status}
                      </Badge>
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
