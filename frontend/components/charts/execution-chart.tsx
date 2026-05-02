"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { day: "Mon", events: 320000 },
  { day: "Tue", events: 448000 },
  { day: "Wed", events: 391000 },
  { day: "Thu", events: 563000 },
  { day: "Fri", events: 674000 },
  { day: "Sat", events: 502000 },
  { day: "Sun", events: 618000 },
];

export function ExecutionChart() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ left: -24, right: 8, top: 10, bottom: 0 }}>
        <defs>
          <linearGradient id="events" x1="0" x2="0" y1="0" y2="1">
            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.5} />
            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid stroke="hsl(var(--border))" vertical={false} />
        <XAxis dataKey="day" tickLine={false} axisLine={false} />
        <YAxis tickLine={false} axisLine={false} />
        <Tooltip
          contentStyle={{
            background: "hsl(var(--card))",
            border: "1px solid hsl(var(--border))",
            borderRadius: 8,
          }}
        />
        <Area
          type="monotone"
          dataKey="events"
          stroke="hsl(var(--primary))"
          fill="url(#events)"
          strokeWidth={2}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
