import { DashboardOverview } from "@/components/dashboard/dashboard-overview";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Button } from "@/components/ui/button";

export default function DashboardPage() {
  return (
    <DashboardShell
      title="Event Pipeline Overview"
      description="Monitor event ingestion, schema validation, aggregate freshness, anomaly signals, and product usage from one internal platform."
      action={<Button>View Events</Button>}
    >
      <DashboardOverview />
    </DashboardShell>
  );
}
