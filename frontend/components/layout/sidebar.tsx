import Link from "next/link";
import {
  Activity,
  BarChart3,
  Database,
  FileJson,
  GitBranch,
  KeyRound,
  Layers,
  LayoutDashboard,
  ListChecks,
  ScrollText,
  Settings,
  TriangleAlert,
} from "lucide-react";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/projects", label: "Projects", icon: Layers },
  { href: "/events", label: "Events", icon: Database },
  { href: "/schemas", label: "Schemas", icon: FileJson },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/funnels", label: "Funnels", icon: GitBranch },
  { href: "/anomalies", label: "Anomalies", icon: TriangleAlert },
  { href: "/pipeline", label: "Pipeline", icon: Activity },
  { href: "/api-keys", label: "API Keys", icon: KeyRound },
  { href: "/audit-logs", label: "Audit Logs", icon: ScrollText },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 border-r bg-card/70 px-4 py-5 lg:block">
      <Link href="/dashboard" className="mb-8 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <ListChecks className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold">EventFlow</p>
          <p className="text-xs text-muted-foreground">Analytics Pipeline</p>
        </div>
      </Link>
      <nav className="space-y-1">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
