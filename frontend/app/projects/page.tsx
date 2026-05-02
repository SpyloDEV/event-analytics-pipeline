import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, Td, Th } from "@/components/ui/table";

const projects = [
  { name: "Product Analytics", key: "product-analytics", events: "3.8M", role: "owner" },
  { name: "Lifecycle", key: "lifecycle", events: "840k", role: "analyst" },
  { name: "Automation", key: "automation", events: "412k", role: "developer" },
];

export default function ProjectsPage() {
  return (
    <DashboardShell
      title="Projects"
      description="Separate ingestion credentials, schemas, funnels, and dashboards by product or application."
      action={<Button>Create Project</Button>}
    >
      <Card>
        <CardHeader>
          <CardTitle>Analytics Projects</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <thead>
              <tr>
                <Th>Name</Th>
                <Th>Key</Th>
                <Th>Events</Th>
                <Th>Role</Th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.key}>
                  <Td className="font-medium">{project.name}</Td>
                  <Td className="font-mono text-muted-foreground">{project.key}</Td>
                  <Td>{project.events}</Td>
                  <Td>
                    <Badge tone="active">{project.role}</Badge>
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
