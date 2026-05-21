"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  ShieldCheck, 
  BarChart3, 
  Activity, 
  Cpu, 
  FileText,
  Search,
  Bell,
  Settings,
  Terminal
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "EXECUTIVE_OVERVIEW", href: "/", icon: LayoutDashboard },
  { name: "TREASURY_COCKPIT", href: "/treasury", icon: BarChart3 },
  { name: "REGULATORY_COCKPIT", href: "/regulatory", icon: ShieldCheck },
  { name: "GOVERNANCE_COCKPIT", href: "/governance", icon: Cpu },
  { name: "AI_COPILOT_CONSOLE", href: "/copilot", icon: Terminal },
  { name: "PLATFORM_OBSERVABILITY", href: "/observability", icon: Activity },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col bg-card border-r border-border">
      <div className="flex h-16 items-center px-6 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-sm flex items-center justify-center">
             <ShieldCheck className="w-5 h-5 text-background" />
          </div>
          <span className="font-heading font-bold text-lg tracking-tight">ESOTERIC BANK</span>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto py-6 px-4">
        <div className="mb-4 px-2">
          <p className="text-[10px] font-bold text-muted-foreground tracking-[0.2em] uppercase">
            Command Domains
          </p>
        </div>
        <nav className="space-y-1">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center px-3 py-2 text-xs font-medium rounded-sm transition-all duration-200",
                pathname === item.href
                  ? "bg-primary/10 text-primary border-l-2 border-primary"
                  : "text-muted-foreground hover:bg-white/5 hover:text-foreground border-l-2 border-transparent"
              )}
            >
              <item.icon
                className={cn(
                  "mr-3 h-4 w-4 flex-shrink-0 transition-colors",
                  pathname === item.href ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
                )}
                aria-hidden="true"
              />
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
      <div className="p-4 border-t border-border bg-black/20">
        <div className="flex items-center gap-3 px-2 py-3 rounded-md">
          <div className="w-8 h-8 rounded-full bg-secondary/20 flex items-center justify-center text-[10px] font-bold text-secondary border border-secondary/30">
            AS
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-[10px] font-bold truncate">AKASH SHARMA</p>
            <p className="text-[9px] text-muted-foreground truncate uppercase tracking-wider">Tier 4 Board</p>
          </div>
        </div>
        <div className="mt-2 text-[8px] text-center text-muted-foreground/50 font-mono">
          INSTITUTIONAL_RESILIENCE_V1.0
        </div>
      </div>
    </div>
  );
}
