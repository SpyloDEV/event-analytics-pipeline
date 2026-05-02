import { ExecutionChart } from "@/components/charts/execution-chart";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AnalyticsPage() {
  return (
    <DashboardShell
      title="Analytics"
      description="Explore event volume, active users, top events, countries, sources, validation failures, and product usage patterns."
    >
      <div className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <KpiCard label="Total events" value="3.8M" delta="+21%" />
          <KpiCard label="Unique users" value="184k" delta="+9%" />
          <KpiCard label="Top event" value="page_viewed" delta="32%" />
          <KpiCard label="Error rate" value="0.08%" delta="-0.03%" />
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Events Over Time</CardTitle>
          </CardHeader>
          <CardContent>
            <ExecutionChart />
          </CardContent>
        </Card>
      </div>
    </DashboardShell>
  );
}
