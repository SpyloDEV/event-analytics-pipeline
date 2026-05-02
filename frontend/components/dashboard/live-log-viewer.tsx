import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const logs = [
  "[10:42:01] event=document_uploaded status=processed project=product-analytics",
  "[10:42:02] schema=document_uploaded validation=passed required=2",
  "[10:42:03] aggregate=events_per_hour bucket=2026-05-02T10 value=18420",
  "[10:42:04] anomaly=payment_failed severity=high signal=volume_spike",
];

export function LiveLogViewer() {
  return (
    <Card>
      <CardHeader>
          <CardTitle>Pipeline Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border bg-slate-950 p-4 font-mono text-xs text-cyan-100">
          {logs.map((line) => (
            <p key={line} className="py-1">
              {line}
            </p>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
