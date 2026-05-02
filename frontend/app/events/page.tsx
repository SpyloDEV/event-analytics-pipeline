import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const events = [
  { name: "document_uploaded", user: "user_123", status: "processed", country: "DE" },
  { name: "workflow_executed", user: "user_123", status: "processed", country: "DE" },
  { name: "payment_failed", user: "user_984", status: "processed", country: "US" },
  { name: "document_uploaded", user: "user_781", status: "failed", country: "FR" },
];

export default function EventsPage() {
  return (
    <DashboardShell
      title="Raw Events"
      description="Inspect accepted, processed, and failed product events with context, properties, and validation state."
    >
      <Card>
        <CardHeader>
          <CardTitle>Recent Events</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Event</Th>
                <Th>User</Th>
                <Th>Status</Th>
                <Th>Country</Th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, index) => (
                <tr key={`${event.name}-${index}`}>
                  <Td className="font-mono font-medium">{event.name}</Td>
                  <Td>{event.user}</Td>
                  <Td>
                    <Badge tone={event.status === "failed" ? "blocked" : "active"}>
                      {event.status}
                    </Badge>
                  </Td>
                  <Td>{event.country}</Td>
                </tr>
              ))}
            </tbody>
          </Table>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}
