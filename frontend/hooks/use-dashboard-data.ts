import { useQuery } from "@tanstack/react-query";

export function useDashboardData() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: async () => ({
      kpis: [
        { label: "Total events", value: "3.8M", delta: "+21%" },
        { label: "Unique users", value: "184k", delta: "+9%" },
        { label: "Events today", value: "302k", delta: "+12%" },
        { label: "Error rate", value: "0.08%", delta: "-0.03%" },
      ],
      activity: [
        "document_uploaded schema validation passed for 18,420 events",
        "workflow_executed aggregate refreshed for production dashboard",
        "payment_failed anomaly detected after hourly volume spike",
        "Activation funnel conversion moved from 41.2% to 44.8%",
      ],
    }),
  });
}
